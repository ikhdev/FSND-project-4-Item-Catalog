from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from sqlalchemy_utils import database_exists, drop_database, create_database

from database_setup import Category  # Category is name of Class in database
from database_setup import CatalogItem  # Item is name of Class in database
from database_setup import Base

engine = create_engine('sqlite:///item_catalog.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


category1 = Category(name="Horror")
session.add(category1)
session.commit()

item1 = CatalogItem(
    name="Gok-seong",
    description=" min:156 | year:2016 ",
    price="18$",
    category=category1)
session.add(item1)
session.commit()

item2 = CatalogItem(
    name="28 Days Later",
    description=" min:113 | year:2002 ",
    price="14$",
    category=category1)
session.add(item2)
session.commit()

item3 = CatalogItem(
    name="Lat den ratte komma in",
    description=" min:115 | year:2008 ",
    price="8$",
    category=category1)
session.add(item3)
session.commit()

item4 = CatalogItem(
    name="Busanhaeng",
    description=" min:118 | year:2016 ",
    price="15$",
    category=category1)
session.add(item4)
session.commit()

item5 = CatalogItem(
    name="The Conjuring",
    description=" min:112 | year:2013 ",
    price="8$",
    category=category1)
session.add(item5)
session.commit()

item6 = CatalogItem(
    name="Pitch Black",
    description=" min:109 | year:2000 ",
    price="9$",
    category=category1)
session.add(item6)
session.commit()

item7 = CatalogItem(
    name="A Quiet Place ",
    description=" min:90 | year:2018 ",
    price="11$",
    category=category1)
session.add(item7)
session.commit()

item8 = CatalogItem(
    name="[Rec]",
    description=" min:78 | year:2007 ",
    price="5$",
    category=category1)
session.add(item8)
session.commit()

category2 = Category(name="Action")
session.add(category2)
session.commit()

item9 = CatalogItem(
    name="The Equalizer",
    description=" min:132 | year:2014 ",
    price="8$",
    category=category2)
session.add(item9)
session.commit()

item10 = CatalogItem(
    name="The Equalizer 2",
    description=" min:121 | year:2018 ",
    price="9$",
    category=category2)
session.add(item10)
session.commit()

item11 = CatalogItem(
    name="Mad Max: Fury Road",
    description=" min:120 | year:2015 ",
    price="13$",
    category=category2)
session.add(item11)
session.commit()

item12 = CatalogItem(
    name="Logan",
    description=" min:137 | year:2017 ",
    price="5$",
    category=category2)
session.add(item12)
session.commit()

item13 = CatalogItem(
    name="Black Panther",
    description=" min:134 | year:2018 ",
    price="16$",
    category=category2)
session.add(item13)
session.commit()

item14 = CatalogItem(
    name="Wonder Woman",
    description=" min:141 | year:2017 ",
    price="3$",
    category=category2)
session.add(item14)
session.commit()

item15 = CatalogItem(
    name="Aquaman",
    description=" min:143 | year:2018 ",
    price="10$",
    category=category2)
session.add(item15)
session.commit()

item16 = CatalogItem(
    name="Dunkirk",
    description=" min:106 | year:2017 ",
    price="7$",
    category=category2)
session.add(item16)
session.commit()

category3 = Category(name="comedy")
session.add(category3)
session.commit()

item17 = CatalogItem(
    name="Step Brothers",
    description=" min:98 | year:2008 ",
    price="14$",
    category=category3)
session.add(item17)
session.commit()

item18 = CatalogItem(
    name="White Chicks",
    description=" min:109 | year:2004 ",
    price="12$",
    category=category3)
session.add(item18)
session.commit()

item19 = CatalogItem(
    name="The Hot Chick",
    description=" min:104 | year:2002 ",
    price="11$",
    category=category3)
session.add(item19)
session.commit()

item20 = CatalogItem(
    name="The Hangover",
    description=" min:100 | year:2009 ",
    price="9$",
    category=category3)
session.add(item20)
session.commit()

item21 = CatalogItem(
    name="Horrible Bosses",
    description=" min:98 | year:2011 ",
    price="5$",
    category=category3)
session.add(item21)
session.commit()
