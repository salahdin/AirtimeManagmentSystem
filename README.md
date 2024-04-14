# Airtime Managment System
##   
- This application aimed to create a web-based platform for corporations to distribute airtime to employees through a USSD code, facilitated by an Android phone connected to RBSoft SMS Gateway.

### installation
- clone or download the repository
- to install all dependencies run
  ```shell
   pip install requirments.txt
  ```
 to run the server run the following commands
 ```shell
 cd AirtimeManagmentSystem
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver
 ```
 on browser go to http://127.0.0.1:8000/
 
 if user wants to create a superuser account (admin),
 run the following command

 ```shell
 python manage.py createsuperuser
 ```
Once logged in go to the admin panel http://127.0.0.1:8000/admin then edit the first config object.

go to https://smsgateway.rbsoft.org/ and create an account, then insert api key on your application.

Follow the instructions on rbsoft website.


