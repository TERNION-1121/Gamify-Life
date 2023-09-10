from utils.config import insert_record
from utils.dbconfig import dbconfig

import datetime

record = ("Academic", 
          "1", 
          "Study the rest two chapters in Hindi!", 
          str(datetime.datetime.now()),
          "NULL")

insert_record(record)

con = dbconfig()
cur = con.cursor()
cur.execute("SELECT * FROM goaldata")
print(cur.fetchall())
con.close()