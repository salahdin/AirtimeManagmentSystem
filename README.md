# AirtimeManagmentSystem
## Descitption 
- This app was an attept to build a webapplication that can be used by corporations to airtime to employees using ussd code via an android phone with rbsoft smsgateway connected.


### installation
- clone or download the repository
- download and install teseract ocr engine 
- to install all dependencies run
  ```shell
   pip install requirments.txt
  ``
 to run the server run the following commands
 ```shell
 cd optss
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver
 ```
 on browser go to http://127.0.0.1:8000/
 
 if user wants to create a superuser account(admin)
 run the following command

 ```shell
 python manage.py createsuperuser
 ```
once loged in go to the admin panel http://127.0.0.1:8000/admin then edit the first config object.

go to https://smsgateway.rbsoft.org/ and create an account then insert api key on your application.

follow the insturctions on rbsoft websie.

