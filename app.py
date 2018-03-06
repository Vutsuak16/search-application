from peewee import *
from flask import Flask, url_for, render_template, request, redirect, session
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from mongoengine import *

mysql_db = MySQLDatabase('sql9224506', user='sql9224506', password='NqDZ2Yd2yg',
                         host='sql9.freemysqlhosting.net', port=3306)

app = Flask(__name__)
app.secret_key = 'very secret key here'

class BaseModel(Model):

    class Meta:
        database = mysql_db

class user(BaseModel):
    id=IntegerField(primary_key=True)
    USERNAME = CharField(max_length=50,unique=True)
    FIRSTNAME = CharField(max_length=50)
    LASTNAME = CharField(max_length=50)
    EMAIL = CharField(max_length=50,unique=True)
    PASSWORD = CharField(max_length=50)
    
    

class login(BaseModel):
    id=IntegerField(primary_key=True)
    USERNAME = CharField(max_length=50,unique=True)
    PASSWORD = CharField(max_length=50)
   

@app.route('/', methods=['GET', 'POST'])
def home():

    if  session.get('logged_in'):
        if request.method == 'POST':
            search = request.form['search']
            s = Search(using=Elasticsearch('https://site:410cc42245545394a3bffceebf1c714c@thorin-us-east-1.searchly.com'),index="newss")
            k = s.query("match", title=search)
            return render_template('results.html',users=k)
        else:
            return render_template('index.html')
    else:
        return render_template('login.html')


       


@app.route('/login', methods=['GET', 'POST'])
def Login():
    
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passwd = request.form['password']
        try:
            l = login.get((login.USERNAME == name) & (login.PASSWORD == passwd)).PASSWORD
            if l is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return "INCORRECT LOGIN"
                

        except:
            return "INCORRECT LOGIN"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        name = request.form['username']
        passwd = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        try:
            
            if name=="" or passwd == "" or firstname== "" or lastname == "" or email == "":
                raise NameError

            user.create(USERNAME=name,FIRSTNAME=firstname,LASTNAME=lastname,EMAIL=email,PASSWORD=passwd)
            login.create(USERNAME=name,PASSWORD=passwd)

        except NameError:
            return "all fields are mandatory"
        except:
            return "username or email already in use"
        

        return render_template('login.html')
    return render_template('register.html')

@app.route("/logout")
def logout():
    
    session['logged_in'] = False
    return redirect(url_for('home'))





if __name__ == '__main__':

   
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)





