# Ballers:: Shreya Roy, Jian Hong Li, Harry Zhu
# SoftDev pd8
# P00
# 2022-11-15
# time spent:

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #facilitate sessions!
from flask import redirect
import os                           #facilitate key generation
import sqlite3
from accounts_db import * #imports account creation functions from accounts_db.py


#______________________
app = Flask(__name__)    #create Flask object
app.secret_key= os.urandom(32) #create random secret key
#print(app.secret_key)


@app.route("/", methods=['GET']) #, methods=['GET', 'POST'])
def index():
    if 'username' in session:   #if already logged in
        return redirect('/home') # username=session['username'], password=session['password'], request_method = "GET")
    else:                       #if not logged in, send user to login page
        return render_template('login.html')


@app.route("/login", methods=['GET','POST'])
def authenticate():
    if (request.method == "POST"):
        session['username']= request.form.get('username')   #remember user in session
        session['password'] = request.form.get('password')  #remember user in session
        if( checkuser(request.form['username'], request.form['password'])):
            #return render_template('home.html', username = request.form['username'], password = request.form['password'], request_method = 'POST',  content = retrieve_stories(request.form['username'])) #response to a form submission
            return redirect('/home')
        else:
            return render_template('login.html', exception =  "Authentication failed, try again")
    else:
        if(session != {}):
            return redirect("/home")
        else:
            return render_template('login.html')

@app.route("/register", methods = ['GET','POST'])
def register():
    if (request.method == "POST"):
        if (request.form.get('password1') != request.form.get('password2')):
            return render_template("register.html", exception = "Passwords don't match")
        elif (request.form.get('password1') == ""):
            return render_template("register.html", exception = "Password can't be empty!")
        else:
            if (create_acc(request.form['username'], request.form['password1'])): #True IF another account exist, false if no problems
                return render_template("register.html", exception = "Username taken!")
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/home")
def homepage():
    if( session != {}):
        content = list(map(int, retrieve_stories(session['username']).split()))
        return render_template('home.html', username = session['username'], password = session['password'], request_method = 'POST',  len = len(content), content = content) #response to a form submission
    else:
        return redirect("/login")

@app.route("/route_content/<string:id>")
def story(id):
    if(session != {}):
        return render_template("content_page.html", title = retrieve_storytitle(id), content = retrieve_storycontent(id), author = session['username'], last_editor = retrieve_storyeditor(id))  
    else:
        return redirect("/login")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        if session != {}:           #if no remembered user, just send to login page
            session.pop('username') #un-remember username
            session.pop('password') #un-remember password
        return render_template('login.html')

@app.route("/create", methods=['GET', 'POST'])
def create():
    if (request.method == "POST"):
        create_story(request.form['title'], request.form['story'], session['username'])
        return redirect("/home")
    else:
        return render_template("create_page.html")

@app.route("/edit/<string:id>", methods=['POST'])
def edit(id):
    return render_template("edit.html", id = id)

@app.route("/editstory/<string:id>", methods=['POST'])
def editstory(id):
    return render_template("edit.html", id = id)
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()


