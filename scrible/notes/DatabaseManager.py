import sqlite3

"""This class initiates a connection to the sqlite database
and returns a cursor object upon quering
"""


class DatabaseManager(object):

    """Connects to database and returns a cursor object
    """

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.commit()
        self.cur = self.conn.cursor()

    """Performs a query to the database based on the supplied
    query string.This method then returns the cursor object to the
    calling class/method
    """

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    """Called when the class object is destroyed.
    """

    def __del__(self):
        # Closes the connection to the database to prevent database locks
        self.conn.close()
