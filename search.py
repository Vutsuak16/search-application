from flask import Flask
from peewee import *


mysql_db = MySQLDatabase('sql9224506', user='sql9224506', password='NqDZ2Yd2yg',
                         host='sql9.freemysqlhosting.net', port=3306)

class BaseModel(Model):

    class Meta:
        database = mysql_db

class user(BaseModel):
    id=IntegerField(primary_key=True)
    USERNAME = CharField(max_length=50)
    FIRSTNAME = CharField(max_length=50)
    LASTNAME = CharField(max_length=50)
    EMAIL = CharField(max_length=50,unique=True)
    PASSWORD = CharField(max_length=50)
    
    

class login(BaseModel):
    id=IntegerField(primary_key=True)
    USERNAME = CharField(max_length=50)
    PASSWORD = CharField(max_length=50)
   
'''
person, created = user.get_or_create(
    first_name=first_name,
    last_name=last_name,
    defaults={'dob': dob, 'favorite_color': 'green'})'''

#user.create(USERNAME='chaplin6',FIRSTNAME='Charlie',LASTNAME="Chaplin",EMAIL="chaplin@gmail.com",PASSWORD="chap43")
#login.create(USERNAME='chaplin6',PASSWORD='chap43')
#havent set username unique as validating both username and password
try:
    l = login.get((login.USERNAME == "chaplin6") & (login.PASSWORD =="chap43")).PASSWORD
    print(l)
except:
    print("register")

try:
    user.create(USERNAME='chaplin6',FIRSTNAME='Charlie',LASTNAME="Chaplin",EMAIL="chaplin@gmail.com",PASSWORD="chap43")
except:
    print("email already in use")


