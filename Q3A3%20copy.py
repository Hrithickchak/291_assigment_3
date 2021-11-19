import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def view(path):
    #this doesnt work

    global connection, cursor
    conn = sqlite3.connect(":memory:")
    # create a connection to the sqlite3 database
    connection = sqlite3.connect(path)
    # create a cursor object which will be used to execute sql statements
    conn.execute('''
    create view ordersize as select order_id as oid, order_item_id as size from order_items group by order_id;
    ''')

def Query2():

    cursor.execute('''
    select oid, avg(size) from ordersize 
    where oid
    in (SELECT order_id  FROM Customers c, Orders o WHERE c.customer_id = o.customer_id AND customer_postal_code = (SELECT c.customer_postal_code FROM  Customers c ORDER BY random() LIMIT 1));
     ''')
    #find a way to print
    s = cursor.fetchall()

    x = []
    # iterate through results to build lists
    for i in s:
        x.append(i[0])
    
    print(x)

# Query 1 using smallDB size
def smallDBQuery():
    db_path = './A3small.db'
    connect(db_path)
    view(db_path)
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
    smallDBQuery()
    mediumDBQuery()
    largeDBQuery()

    #call all queries 
    #optimize queries 
    #make a graph

if __name__ == "__main__":
    main()