import sqlite3
import matplotlib.pyplot as plt
import numpy as np

#from Createdb import smallDB 
#Given a random customer_postal_code from Customers, 
#find how many orders have been placed by customers 
#who have that customer_postal_code.

#main query call
def Query1():

    global connection, cursor

    cursor.execute( '''
    SELECT COUNT(order_id) 
    FROM Customers C, Orders O 
    WHERE C.customer_id = O.customer_id AND
    customer_postal_code = (SELECT C.customer_postal_code 
    FROM Customers C ORDER BY random() LIMIT 1);''')
    
    #print to check
    s = cursor.fetchall()

    x = []
    # iterate through results to build lists
    for i in s:
        x.append(i[0])
    
    print(x)

# Query 1 using smallDB size
def smallDBQuery():
    db_path = './A3Small.db'
    connect(db_path)
    Query1()
    connection.close()
# Query 1 using mediumDB size
def mediumDBQuery():
    db_path = './A3Medium.db'
    connect(db_path)
    Query1()
    connection.close()
# Query 1 using mediumDB size
def largeDBQuery():
    db_path = './A3Large.db'
    connect(db_path)
    Query1()
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