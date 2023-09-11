import sqlite3
import os

class DataBase():
    path = '/'.join([os.getcwd(), 'gli.db'])
    def __init__(self) -> None:
        self._connection    = sqlite3.connect(DataBase.path, detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
        self.cursor         = self._connection.cursor()

    def is_empty(self) -> bool:
        # Query the database to check for tables 
        self.cursor.execute("""SELECT count(name) FROM sqlite_master 
                            WHERE type = 'table' 
                            AND (name = 'userdata' OR name = 'goaldata');""")
        return self.cursor.fetchone()[0] == 0

    def create_tables(self) -> None:
        if self.is_empty(): # No tables exist
            self.cursor.execute("""CREATE TABLE userdata (
                        first_name      TEXT        NOT NULL,
                        middle_name     TEXT,
                        last_name       TEXT,
                        exp_pts         INTEGER
                        )""")

            self.cursor.execute("""CREATE TABLE goaldata (
                        goal_type       TEXT        NOT NULL,
                        tier            TEXT        NOT NULL,
                        goal_details    TEXT        NOT NULL,
                        start_time      TIMESTAMP   NOT NULL,
                        end_time        TIMESTAMP
                        )""")
            
            self.commit()
    
    def insertUserName(self, first_name, middle_name, last_name) -> None:
        self.cursor.execute("INSERT INTO userdata VALUES(?, ?, ?, 0)", (first_name, middle_name, last_name))
        self.commit()

    def commit(self) -> None:
        self._connection.commit()
    
db = DataBase()