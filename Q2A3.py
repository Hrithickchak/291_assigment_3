import sqlite3
import matplotlib.pyplot as plt
import numpy as np

#from Createdb import smallDB 

def Query2():

    global connection, cursor

    cursor.execute('''CREATE VIEW OrderSize(oid, size)
    AS SELECT order_id, order_item_id    
	FROM Orders o, Order_items i
     ''')
    #find a way to print 
    s = cursor.fetchone()
    print(s)

# Query 1 using smallDB size
def smallDBQuery():
    db_path = './A3small.db'
    connect(db_path)
    Query2()
    connection.close()
# Query 1 using mediumDB size
def mediumDBQuery():
    db_path = './A3medium.db'
    connect(db_path)
    Query2()
    connection.close()
# Query 1 using mediumDB size
def largeDBQuery():
    db_path = './A3large.db'
    connect(db_path)
    Query2()
    connection.close()


def connect(path):
    # using global variables already defined in main method, not new variables
    global connection, cursor
    # create a connection to the sqlite3 database
    connection = sqlite3.connect(path)
    # create a cursor object which will be used to execute sql statements
    cursor = connection.cursor()
    # execute a sql statement to enforce foreign key constraint
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    # commit the changes we have made so they are visible by any other connections
    connection.commit()
    return

def main():
    global connection

    smallDBQuery()
    mediumDBQuery()
    largeDBQuery()

    #call all queries 
    #optimize queries 
    #make a graph

if __name__ == "__main__":
    main()