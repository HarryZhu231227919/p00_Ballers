# Ballers:: Shreya Roy, Jian Hong Li, Harry Zhu
# SoftDev pd8
# K19: session
# 2022-11-7
# time spent: 2.5 hours

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #facilitate sessions!
from flask import redirect
import os                           #facilitate key generation
import sqlite3

#DB_FILE = "PAGES"
#db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
#c = db.cursor()

#command = "CREATE TABLE rosters(name TEXT, mark INTEGER);"
# test SQL stmt in sqlite3 shell, save as string
#c.execute(command)    # run SQL statement

#db.commit() #save changes
#db.close()  #close database

#______________________

app = Flask(__name__)    #create Flask object
app.secret_key= os.urandom(32) #create random secret key
#print(app.secret_key)

correctuser = "user"
correctpw = "correct!"

@app.route("/", methods=['GET']) #, methods=['GET', 'POST'])
def index():
    if 'username' in session:   #if already logged in
        return render_template('/home') # username=session['username'], password=session['password'], request_method = "GET")
    else:                       #if not logged in, send user to login page
        return render_template('login.html')


@app.route("/login", methods=['GET','POST'])
def authenticate():
    session['username']= request.form.get('username')   #remember user in session
    session['password'] = request.form.get('password')  #remember user in session
    if(correctuser == request.form['username'] and correctpw == request.form['password']):
        return render_template('home.html', username = request.form['username'], password = request.form['password'], request_method = 'POST') #response to a form submission
    else:
        return render_template('login.html', exception =  "Authentication failed, try again")

@app.route("/register", methods = ['GET','POST'])
def register():
    return render_template("register.html")

@app.route("/create_account", methods = ['GET','POST'])
def create_account():
    if (request.form.get('password1') != request.form.get('password2')):
        return render_template("register.html", exception = "Passwords don't match")
    return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        if session != {}:           #if no remembered user, just send to login page
            session.pop('username') #un-remember username
            session.pop('password') #un-remember password
        return render_template('login.html')



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
