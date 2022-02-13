# momox-backend

This is backend api for creating orders using xml file.
To Run this application you need:
  1: python 3.6 with pip
  2: then Run pip install pip install -r requirements.txt
  3: python app.py
Hit POST api using following link:
POST {base_url}/orders with employee_orders.xml

TODO:
    ->Need to create React app which provide frontend application to post file and hit this request
    ->Need to configure ngnix, npm and gunicorn to deploy application on server
