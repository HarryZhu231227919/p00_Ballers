import sqlite3

DB_FILE = "ACCOUNT.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("CREATE TABLE if not Exists users(username TEXT, password TEXT);")
c.execute("CREATE TABLE if not Exists stories(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, username TEXT);")
c.execute("CREATE TABLE if not Exists story_content(id INTEGER, content TEXT, last_editedby TEXT);")

db.commit()
db.close()
    

def checkuser(username, password): #checks if user's login is correct
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username = ?;', [username])
    correct_password = c.fetchone() #fetches correct password from tuple
    if correct_password is None:
        return False
    else:
        return password == correct_password[0]
        
        
#returns TRUE if another account exists with user, otherwise creates acc
def create_acc(username, password): 
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT username FROM users WHERE username = ?;', [username])
    check_user = c.fetchone();
    if check_user is None:
        c.execute('INSERT INTO users VALUES (?, ?);', (username, password) )
        db.commit()
        return False
    else:
        return True

def create_story(title, content, username): #adds story to database with unique ID
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('INSERT INTO stories(title, username) VALUES (?, ?);', (title, username) )
    c.execute("SELECT id FROM stories ORDER BY id DESC LIMIT 1;")
    id = c.fetchone();
    id = int(''.join(map(str, id)))         #scuffed
    c.execute('INSERT INTO story_content VALUES (?, ?, ?);', (id, content, username))
    db.commit()
    return True
    
def retrieve_stories(username): # retrieve all story IDs created by user
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT id FROM stories WHERE username = ?;', [username])
    stories = c.fetchall();
    return " ".join("%s" % tup for tup in stories) #scuffed

def retrieve_storytitle(id): # retrieve title of story using ID
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT title FROM stories WHERE id = ?;', [id])
    title = c.fetchone();
    return title[0]
    
def retrieve_storycontent(id):  # retrieve most recent content of story using ID
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #c.execute('SELECT content FROM story_content WHERE id = ?;', [id])
    c.execute('SELECT content FROM story_content WHERE id = ? ORDER BY LENGTH(content) DESC LIMIT 1;', [id])
    content = c.fetchone();
    return content[0]

def retrieve_storyeditor(id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #c.execute('SELECT content FROM story_content WHERE id = ?;', [id])
    c.execute('SELECT last_editedby FROM story_content WHERE id = ? ORDER BY LENGTH(content) DESC LIMIT 1;', [id])
    content = c.fetchone();
    return content[0]

def addto_story(id, content, username): # needs story ID (url), new content, and username
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    old = retrieve_storycontent(id)
    c.execute('SELECT last_editedby FROM story_content WHERE id = ? AND last_editedby = ?;', (id, username))
    oldedit = c.fetchone();
    if(username == oldedit[0]):
        return True
    else:
        c.execute('INSERT INTO story_content VALUES (?, ?, ?);', (id, old + " " + content, username))
        db.commit()
        return False
    
    
def all_stories(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT id FROM stories WHERE username != ?;', [username])
    stories = c.fetchall();
    return " ".join("%s" % tup for tup in stories) #scuffed


#function not currently being used for anything, might be helpful in future
# returns number of stories (int) that user authored
def num_ofstories(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM stories WHERE username = ?;', [username])
    content = c.fetchone();
    return content[0]