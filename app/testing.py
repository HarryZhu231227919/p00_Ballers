import sqlite3
from accounts_db import * #imports account creation functions from accounts_db.py

#create_story("cinderella", "once upon a time", "user")
#create_story("belle and the beast", "once upon a time", "user")
#create_story("idk lol", "lol idk", "user")

print(retrieve_stories("user"))

print(all_stories("user2"))

print(retrieve_storytitle(2))

print(retrieve_storycontent(2))

#addto_story(1, "oncieuponatime", "user2")
