import sqlite3

def dbconfig():
    # Create a database
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    try:    # Create Tables
        cur.execute("""CREATE TABLE userdata (
                    exp_pts INTEGER
                    )""")
        cur.execute("INSERT INTO userdata VALUES(0)")

        cur.execute("""CREATE TABLE goaldata (
                    goal_type       TEXT        NOT NULL,
                    tier            TEXT        NOT NULL,
                    goal_details    TEXT        NOT NULL,
                    start_time      TEXT        NOT NULL,
                    end_time        TEXT
                    )""")
        con.commit()
    except: # Tables already exist
        pass

    return con