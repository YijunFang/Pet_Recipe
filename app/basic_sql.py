#!/usr/bin/python
from __future__ import print_function
import sqlite3
import glob
import re

conn = sqlite3.connect('db/recipedb.db')
conn.text_factory = str
print("Opened database successfully")

# select
cureor=conn.execute("select * from user;")
for row in cureor:
   print("id =", str(row[0]),end='')
   print("user_name =", row[1],end='')
   print("password =", row[2],end='')
   print("email =", str(row[3]))

print("Operation done successfully")

# update
conn.execute("UPDATE user set user_name ='whattt' where ID = 1")
conn.commit()
cureor=conn.execute("select * from user where id ==1;")
for row in cureor:
   print("id =", str(row[0]),end='')
   print("user_name =", row[1],end='')
   print("password =", row[2],end='')
   print("email =", str(row[3]))
print("Update done successfully")

#delete
conn.execute("DELETE from user where user_name=='jane';")
conn.commit()
print("Total number of rows deleted :", conn.total_changes)

#INSERT
conn.execute("INSERT INTO user ('user_name','password','email') \
      VALUES ('jane','pwd','135@gmail.com')");
conn.execute("INSERT INTO user ('user_name','password','email') \
      VALUES ('aa','pwd','aa@gmail.com')");
conn.execute("INSERT INTO user ('user_name','password','email') \
      VALUES ('bb','pwd','bb@gmail.com')");
conn.execute("INSERT INTO user ('user_name','password','email') \
      VALUES ('cc','pwd','cc@gmail.com')");
conn.commit()
print("Records created successfully")

conn.close()
