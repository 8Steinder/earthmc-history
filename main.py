import os
import sys
import time
from apihandler import playerssave
from history import record_changes
from playerdb import startupinsert, startuptable

db_file = "Player.db"

if os.path.exists(db_file):
  print("Found DB.")
else:
  print("Error! DB doesn't exist.")
  question = input("Do you want to create a new DB? y/n: ")
  if question.lower() != "y":
    print("Stopping startup")
    sys.exit()

  startuptable()
  playerssave()
  startupinsert()
  print("Data fetched, DB with tables created and startup insert done.")
while True:
  playerssave()
  record_changes()
  time.sleep(15)