import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time
connection = None
cursor = None
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

def Query2(postal):
    global connection, cursor
    
    view = '''
    create view ordersize as select order_id as oid, COUNT(DISTINCT order_item_id) as size from order_items group by order_id;
    '''
    cursor.execute(view)
    
    connection.commit()
    q = '''
    select oid, avg(ordersize.size) from Orders, Customers, ordersize 
    where Orders.customer_id = Customers.customer_id
    AND Customers.customer_postal_code = :postal AND ordersize.oid = Orders.order_id
    '''
    #find a way to print
    #cursor.execute(q ,{'postal' :postal})
    s = cursor.fetchall()
    
    x = []
    y = []
    # iterate through results to build lists
    for i in s:
        x.append(i[0])
        y.append(i[1])
    
    print(x)
    cursor.execute('''DROP VIEW ordersize''')
    connection.commit()

# Query 1 using smallDB size
def smallDBQuery(postal):
    db_path = './A3small.db'
    connect(db_path)
    Query2(postal)
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

def main():
    smallDBQuery(95020)
    #mediumDBQuery()
    #largeDBQuery()

    #call all queries 
    #optimize queries 
    #make a graph

if __name__ == "__main__":
    main()