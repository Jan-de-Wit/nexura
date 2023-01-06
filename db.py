import os
import sqlite3


def dbConn(dbPath):
    """ Returns a connection to the database """
    if not os.path.exists(dbPath):
        print(f"Error: Database does not exist. Path: {dbPath}")
        return None
    return sqlite3.Connection(dbPath)
