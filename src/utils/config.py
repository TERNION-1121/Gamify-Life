import sqlite3
from utils.dbconfig import dbconfig


def insert_record(item: tuple):
    con = dbconfig()
    cur = con.cursor()
    cur.execute("INSERT INTO goaldata VALUES(?,?,?,?,?)", item)
    con.commit()
