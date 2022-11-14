import sqlite3
from accounts_db import * #imports account creation functions from accounts_db.py

create_story("cinderella", "once upon a time", "user")
create_story("belle and the beast", "once upon a time", "user")
create_story("idk lol", "lol idk", "user")

print(retrieve_stories("user"))

#print(retrieve_storytitle(1))
