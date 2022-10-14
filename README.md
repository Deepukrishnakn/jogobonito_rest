
# Turf booking ecommerce-django
This is a sample application that demonstrates an e-commerce turf booking website using the React.js The application loads turf from a PostgreSQL database and displays them. Users can select to display turf in a single category. Users can register and login to website and, click on any turf to get more information including pricing. Users can select slot and add them to their complete their payment using Razor-pay or cod. They can view their order status. In admin side, admins can manage users,Vendor and In Vendor side, vendor can manage turf,sloat and CRUD etc...


## Live Demonstration

The E-commerce demo can be viewed online here: https://jogobonito.bootit.tk

Here is the screencast that show the E-commerce demo application in use: https://jogobonito.tk


## Getting started
To get started you can simply clone this ecommerce-django repository and install the dependencies.

Clone the ecommerce-demo repository using git:
```python
git clone https://github.com/Deepukrishnakn/jogobonito_rest.git
cd ecommerce-django
```
Create a virtual environment to install dependencies in and activate it:
```python
python3 -m venv myenv
source myenv/bin/activate
```

Then install the dependencies:
```python
(myenv)$ pip install -r requirements.txt
```
Note the ```(myenv)``` in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once ```pip``` has finished downloading the dependencies:
```python
(myenv)$ cd ecommerce-django
(myenv)$ python3 manage.py runserver
```
And navigate to ```http://127.0.0.1:8000/```


## Tech Stack
  Python
  
  Django restframework
  
  PostgreSQL
  
  Bootstrap
  
  MUI
  
  Javascript
