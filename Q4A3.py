import sqlite3
import matplotlib.pyplot as plt
import numpy as np
# Given a random order_id from Orders, 
# find in how many (unique) postal codes (i.e., cities) 
# are the sellers that fulfilled that order.
# main query call
def Query4():

    global connection, cursor

    cursor.execute( '''
        SELECT count(DISTINCT s.seller_postal_code)  
        FROM Order_items i, Sellers s 
        WHERE i.order_id = (SELECT o_i.order_id FROM  Order_items o_i ORDER BY random() LIMIT 1)
        AND i.seller_id = s.seller_id
   ''')
    
    #print to check
    s = cursor.fetchone()
    print(s)

# Query 1 using smallDB size
def smallDBQuery():
    db_path = './A3Small.db'
    connect(db_path)
    Query4()
    connection.close()
# Query 1 using mediumDB size
def mediumDBQuery():
    db_path = './A3Medium.db'
    connect(db_path)
    Query4()
    connection.close()
# Query 1 using mediumDB size
def largeDBQuery():
    db_path = './A3Large.db'
    connect(db_path)
    Query4()
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