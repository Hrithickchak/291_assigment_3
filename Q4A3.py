import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time
#initialize uni self and user arrays
uni=[]
self=[]
user=[]
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
    #s = cursor.fetchall()

    #x = []
    # iterate through results to build lists
    #for i in s:
        #x.append(i[0])

def uniformed():
    cursor.execute('PRAGMA automatic_index =False')
    cursor.execute('PRAGMA foreign_keys=OFF;')
    cursor.execute('''CREATE TABLE IF NOT EXISTS CustomersNew (
                        "customer_id" TEXT,
                        "customer_postal_code" INTEGER);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS OrdersNew(
                        "order_id" TEXT, 
                        "customer_id" Text);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS SellersNew(
                        "seller_id" TEXT, 
                        "seller_postal_code" INTEGER);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Order_itemsNew(
                        "order_id" TEXT, 
                        "order_item_id" INTEGER,
                        "product_id" TEXT,
                        "seller_id" TEXT);''')


    cursor.execute('''INSERT INTO CustomersNew
                        SELECT customer_id, customer_postal_code 
                        FROM Customers;''')
    cursor.execute('''INSERT INTO OrdersNew 
                        SELECT order_id, customer_id
                        FROM Orders;''')
    cursor.execute('''INSERT INTO SellersNew 
                        SELECT seller_id, seller_postal_code
                        FROM Sellers;''')
    cursor.execute('''INSERT INTO Order_itemsNew 
                        SELECT order_id, order_item_id, product_id, seller_id
                        FROM Order_items;''')

#rename is execute so that each table is unique when ran 50 times
    cursor.execute('''ALTER TABLE Customers RENAME TO CustomersOrg;''')
    cursor.execute('''ALTER TABLE Orders RENAME TO OrdersOrg;''')
    cursor.execute('''ALTER TABLE Sellers RENAME TO SellersOrg;''')
    cursor.execute('''ALTER TABLE Order_items RENAME TO Order_itemsOrg;''')

    cursor.execute('''ALTER TABLE CustomersNew RENAME TO Customers;''')
    cursor.execute('''ALTER TABLE OrdersNew RENAME TO Orders;''')
    cursor.execute('''ALTER TABLE SellersNew RENAME TO Sellers;''')
    cursor.execute('''ALTER TABLE Order_itemsNew RENAME TO Order_items;''')
def self_opt():
    cursor.execute('PRAGMA automatic_index=True;')
    cursor.execute('PRAGMA foreign_keys=ON;')
def user_opt():
    self_opt()
    cursor.execute('''DROP INDEX IF EXISTS o_index;''')
    cursor.execute('''CREATE INDEX o_index ON Orders(order_id)''')
#collectTime function runs the list 50 times and outputs the average time for each database
def collectTime():
    runningTimeList = []
    for i in range (50):
        start = time.time()
        Query4()
        end = time.time()
        runningTime = end - start
        runningTimeList.append(runningTime)
    avgTime = sum(runningTimeList)*1000/50
    return avgTime
#drop() drops all old tables and replaces them with the original names 
def drop():
    cursor.execute('''DROP TABLE IF EXISTS Customers;''')
    cursor.execute('''DROP TABLE IF EXISTS Orders;''')
    cursor.execute('''DROP TABLE IF EXISTS Sellers;''')
    cursor.execute('''DROP TABLE IF EXISTS Order_items;''')
    cursor.execute('''ALTER TABLE CustomersOrg RENAME TO Customers;''')
    cursor.execute('''ALTER TABLE OrdersOrg RENAME TO Orders;''')
    cursor.execute('''ALTER TABLE SellersOrg RENAME TO Sellers;''')
    cursor.execute('''ALTER TABLE Order_itemsOrg RENAME TO Orders_items;''')

# The definitions for each query is defined here. This is also where self, user and uniformed is ran

# Query 4 using smallDB size
def smallDBQuery():
    #uniformed
    db_path = './A3Small.db'
    connect(db_path)
    uniformed()
    uni.append(collectTime())
    drop()
    connection.close()
    #self-optimization
    db_path = './A3Small.db'
    connect(db_path)
    self_opt()
    self.append(collectTime())
    connection.close()
    #user-optimization
    db_path = './A3Small.db'
    connect(db_path)
    user_opt()
    user.append(collectTime())
    connection.close()
# Query 4 using mediumDB size 
def mediumDBQuery():
    #uniformed
    db_path = './A3Medium.db'
    connect(db_path)
    uniformed()
    uni.append(collectTime())
    drop()
    connection.close()
    #self-optimization
    db_path = './A3Medium.db'
    connect(db_path)
    self_opt()
    self.append(collectTime())
    connection.close()
    #user-optimization
    db_path = './A3Medium.db'
    connect(db_path)
    user_opt()
    user.append(collectTime())
    connection.close()
   
# Query 4 using largeDB size
def largeDBQuery():
    #uniformed
    db_path = './A3Large.db'
    connect(db_path)
    uniformed()
    uni.append(collectTime())
    drop()
    connection.close()
    #self-optimization
    db_path = './A3Large.db'
    connect(db_path)
    self_opt()
    self.append(collectTime())
    connection.close()
    #user-optimization
    db_path = './A3Large.db'
    connect(db_path)
    user_opt()
    user.append(collectTime())
   
    connection.close()
    print(uni)
    print(self)
    print(user)

# connect path is from MA5 example code. this brings in the connection for path
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

# plot takes uni, self and user and graphs them in a bar graph
def plot():
    labels=["small","medium","large"]
    fig,ax=plt.subplots()
    ax.bar(labels,uni,0.5,label='uniformed')
    ax.bar(labels,self,0.5,bottom=uni,label='self-optimization')
    ax.bar(labels,user,0.5,bottom = list(map(lambda x,y: x+y, uni, self)) ,label='user-optimization')
    ax.set_ylabel('time (ms)')
    ax.set_title('Query 4 (runtime in ms)')
    ax.legend()

    #plt.show()
    path = './{}chart.png'.format('Q4A3')
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    plt.close()

def main():
    global connection

    smallDBQuery()
    mediumDBQuery()
    largeDBQuery()
    plot()
    #call all queries 
    #optimize queries 
    #make a graph


if __name__ == "__main__":
    main()