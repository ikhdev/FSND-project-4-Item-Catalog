import requests
from flask import make_response
import json
import httplib2
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
import string
import random
from flask import session as login_session
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User
from flask import Flask, request, render_template
from flask import redirect, url_for, flash, jsonify
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


engine = create_engine('sqlite:///items_catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# jsonify categories.
@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# jsonify item.
@app.route('/category/<int:ID>/items/<int:itemID>/JSON')
def itemJSON(ID, itemID):
    item = session.query(CatalogItem).filter_by(
        id=itemID, category_id=ID).one()
    return jsonify(item=item.serialize)


# list of items.
@app.route('/category/<int:ID>/items/JSON')
def itemsJSON(ID):
    items = session.query(CatalogItem).filter_by(category_id=ID).all()
    return jsonify(items=[i.serialize for i in items])


# all catalog data.
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    categoryJSON = [c.serialize for c in categories]
    for c in range(len(categoryJSON)):
        items = [i.serialize for i in session.query(CatalogItem).filter_by(
            category_id=categoryJSON[c]["id"]).all()]
        if items:
            categoryJSON[c]["i"] = items
    return jsonify(Category=categoryJSON)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """
    style = "width: 300px;
             height: 300px;
             border-radius: 150px;
             -webkit-border-radius: 150px;
             -moz-border-radius: 150px;">
            """
    flash("you are now logged in as %s" % login_session['username'])
    return output


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/category')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


engine = create_engine('sqlite:///item_catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Display all categories
@app.route('/')
@app.route('/category/')
def displayCategory():
    categories = session.query(Category).all()
    return render_template('displayCategory.html', categories=categories)

#################################################
# CRUD for Category
#################################################

# add new Category


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please add name')
            return redirect(url_for('newCategory'))
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("new category created!")
        return redirect(url_for('displayCategory'))
    else:
        categories = session.query(Category).all()
        return render_template('newCategory.html', categories=categories)

# edit Category


@app.route('/category/<int:ID>/edit/', methods=['GET', 'POST'])
def editCategory(ID):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=ID).one()
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this category. Please create your own category in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if not request.form['name']:
            flash('Can not be empty , enter other name in the blank')
            return redirect(url_for('editCategory', ID=ID))
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash("Category edited!")
        return redirect(url_for('displayCategory', ID=ID))
    else:
        return render_template(
            'editCategory.html',
            ID=ID,
            category=editedCategory)

# Delete Category


@app.route('/category/<int:ID>/delete/', methods=['GET', 'POST'])
def deleteCategory(ID):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id=ID).one()
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':

        session.delete(categoryToDelete)
        session.commit()
        flash("Category deleted!")
        return redirect(url_for('displayCategory', ID=ID))
    else:
        return render_template(
            'deleteCategory.html',
            category=categoryToDelete)

#################################################
# CRUD for Item
#################################################

# Display all Items


@app.route('/category/<int:ID>/')
@app.route('/category/<int:ID>/items/')
def displayItem(ID):
    categories = session.query(Category).filter_by(id=ID).one()
    items = session.query(CatalogItem).filter_by(category_id=ID).all()
    return render_template(
        'displayItem.html',
        categories=categories,
        items=items)


# New Item


@app.route('/category/<int:ID>/item/new/', methods=['GET', 'POST'])
def newItem(ID):
    categories = session.query(Category).filter_by(id=ID).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categories.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this category. Please create your own category.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if not request.form['name']:
            flash('Can not be empty , enter other name in the blank')
            return redirect(url_for('newItem', ID=ID))
        newItem = CatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            category_id=ID, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("new item created!")
        return redirect(url_for('displayItem', ID=ID))
    else:
        return render_template('newItem.html', ID=ID, categories=categories)

# Edit Item


@app.route('/category/<int:ID>/<int:itemID>/edit/', methods=['GET', 'POST'])
def editItem(ID, itemID):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=ID).one()
    editedItem = session.query(CatalogItem).filter_by(id=itemID).one()
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this category. Please create your own category in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if not request.form['name']:
            flash('Can not be empty , enter other name in the blank')
            return redirect(url_for('editItem',
                                    ID=ID, itemID=itemID))
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']

        session.add(editedItem)
        session.commit()
        flash("Item edited!")
        return redirect(url_for('displayItem', ID=ID))
    else:
        return render_template(
            'editItem.html',
            ID=ID,
            itemID=itemID,
            item=editedItem,
            categories=categories)

# Delete Item


@app.route('/category/<int:ID>/<int:itemID>/delete/', methods=['GET', 'POST'])
def deleteItem(ID, itemID):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(id=ID).one()
    itemToDelete = session.query(CatalogItem).filter_by(id=itemID).one()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('displayItem', ID=ID))
    else:
        return render_template(
            'deleteItem.html',
            item=itemToDelete,
            categories=categories)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
