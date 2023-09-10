import sqlite3

class DataBase():
    def __init__(self, dbName) -> None:
        self._connection = sqlite3.connect(f'{dbName}.db', detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
        self.cursor = self.connection.cursor()

    def create_tables(self) -> None:
        try:    # Create Tables
            self.cursor.execute("""CREATE TABLE userdata (
                        name    TEXT        NOT NULL,
                        exp_pts INTEGER
                        )""")

            self.cursor.execute("""CREATE TABLE goaldata (
                        goal_type       TEXT        NOT NULL,
                        tier            TEXT        NOT NULL,
                        goal_details    TEXT        NOT NULL,
                        start_time      TIMESTAMP   NOT NULL,
                        end_time        TIMESTAMP
                        )""")
            
            self.connection.commit()

        except: # Tables already exist
            pass    
    
    @property
    def getConnectionObject(self) -> None:
        return self._connection