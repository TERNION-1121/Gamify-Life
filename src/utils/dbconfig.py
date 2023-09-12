import sqlite3
import os

class DataBase():
    def __init__(self) -> None:
        self._connection    = sqlite3.connect('/'.join([os.getcwd(), 'gli.db']))
        self.cursor         = self._connection.cursor()

    def is_empty(self) -> bool:
        # query the database to check for tables 
        self.cursor.execute("""SELECT count(name) FROM sqlite_master 
                            WHERE type = 'table' 
                            AND (name = 'userdata' OR name = 'goaldata');""")
        return self.cursor.fetchone()[0] == 0

    def create_tables(self) -> None:
        if self.is_empty(): # no tables exist
            self.cursor.execute("""CREATE TABLE userdata (
                        first_name      TEXT        NOT NULL,
                        middle_name     TEXT,
                        last_name       TEXT,
                        exp_pts         INTEGER
                        )""")

            self.cursor.execute("""CREATE TABLE goaldata (
                        type            TEXT        NOT NULL,
                        tier            TEXT        NOT NULL,
                        description     TEXT        NOT NULL,
                        status          TEXT        NOT NULL,
                        start_time      TIMESTAMP   NOT NULL,
                        end_time        TIMESTAMP
                        )""")
            
            self.commit()

    def insertUserName(self, first_name, middle_name, last_name) -> None:
        self.cursor.execute("INSERT INTO userdata VALUES(?, ?, ?, 0)", (first_name, middle_name, last_name))
        self.commit()

    def getUserName(self) -> tuple:
        self.cursor.execute("SELECT first_name, middle_name, last_name FROM userdata")
        return self.cursor.fetchone()

    def getExperiencePts(self) -> int:
        self.cursor.execute("SELECT exp_pts from userdata")
        return self.cursor.fetchone()[0]
    
    def insert_goal_record(self, record) -> None:
        self.cursor.execute("INSERT INTO goaldata VALUES(?, ?, ?, ?, ?, ?)", record)
        self.commit()

    def get_all_goals(self, goal_status=None):
        if goal_status == "In Progress":
            return self.cursor.execute("SELECT rowid, * FROM goaldata WHERE status='In Progress'").fetchall()
        elif goal_status == "Completed":
            return self.cursor.execute("SELECT rowid, * FROM goaldata WHERE status='Completed'").fetchall()
        elif goal_status == "Dumped":
            return self.cursor.execute("SELECT rowid, * FROM goaldata WHERE status='Dumped'").fetchall()
        else:
            return self.cursor.execute("SELECT rowid, * FROM goaldata").fetchall()
    
    def set_goal_finish(self, goalID: int, dt: str):
        self.cursor.execute("UPDATE goaldata SET end_time='?', status='Completed' WHERE rowid=?", (dt, goalID))
        self.commit()
    
    def drop_goal_record(self, goalID: int):
        self.cursor.execute("DELETE FROM goaldata WHERE rowid=?", (goalID))
        self.commit()

    def commit(self) -> None:
        self._connection.commit()
    
db = DataBase()