# FSND-project-4-Item-Catalog

## Skills:
1.Python <br />
2.HTML <br />
3.CSS <br />
4.OAuth <br />
5.Flask Framework<br />
<br />
## Dependencies:
[Vagrant](https://www.vagrantup.com/)<br />
[Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)<br />
[VirtualBox](https://www.virtualbox.org/wiki/Downloads)<br />
<br />
## How to Install
1.Install Vagrant & VirtualBox.<br />
2.Clone the Udacity virtual machine Virtual Machine.<br />
3.Clone this repository.<br />
4.Launch the Vagrant VM ```vagrant up```.<br />
5.Log into Vagrant VM ```vagrant ssh```.<br />
6.Navigate to cd/vagrant as instructed in terminal<br />
7.run ``` sudo pip install requests ```.<br />
8.Setup application database ```python database_setup.py ```.<br />
9.fill the database ```python fakedata.py ```.<br />
10.Run application using ```python application.py ```.<br />
11.open up the browser to ```http://localhost:8000```.<br />
<br />
## JSON
Catalog JSON: ```/catalog/JSON``` - lists all categories in the app.<br />
Categories JSON: ```/category/<int:ID>/items/<int:itemID>/JSON``` - lists specific category items.<br />
Category Items JSON: ```/category/<int:ID>/items/JSON``` - Lists specific category items list.<br />
Category Item JSON: ```/catalog/JSON``` - Lists specific category item details.<br />
<br />
## Screenshots
<img src="/screenshots/1.png">
<img src="/screenshots/2.png">
<img src="/screenshots/3.png">
<img src="/screenshots/4.png">
<img src="/screenshots/5.png">
<img src="/screenshots/6.png">
<img src="/screenshots/7.png">
<img src="/screenshots/8.png">
<img src="/screenshots/9.png">
