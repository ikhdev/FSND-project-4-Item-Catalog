# FSND-project-4-Item-Catalog

## Skills:
1.Python <br />
2.HTML <br />
3.CSS <br />
4.OAuth <br />
5.Flask Framework<br />

## Dependencies:
-[Vagrant](https://www.vagrantup.com/)
-[Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
-[VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## How to Install
1.Install Vagrant & VirtualBox.
2.Clone the Udacity virtual machine Virtual Machine.
3.Clone this repository.
4.Launch the Vagrant VM ```vagrant up```.
5.Log into Vagrant VM ```vagrant ssh```.
6.Navigate to cd/vagrant as instructed in terminal
7.run ``` sudo pip install requests ```.
8.Setup application database ```python database_setup.py ```.
9.fill the database ```python fakedata.py ```.
10.Run application using ```python application.py ```.
11.open up the browser to ```http://localhost:8000```.

## JSON
Catalog JSON: /catalog/JSON - lists all categories in the app.
Categories JSON: /category/<int:ID>/items/<int:itemID>/JSON - lists specific category items.
Category Items JSON: /category/<int:ID>/items/JSON - Lists specific category items list.
Category Item JSON: /catalog/JSON - Lists specific category item details.
