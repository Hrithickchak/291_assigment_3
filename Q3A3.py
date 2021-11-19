import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time
import random
uni=[]
self=[]
user=[]
#main query call
def Query3(postal):

    global connection, cursor

    query = ''' SELECT COUNT(*), AVG(OS.size)
                FROM Orders O, Customers C, ( SELECT order_id as oid, COUNT(DISTINCT order_item_id) as size FROM Order_items O GROUP BY O.order_id )as OS
                WHERE O.customer_id = C.customer_id
                AND C.customer_postal_code=:postal
                AND OS.oid=O.order_id
            '''
    t1 = time.process_time()
    cursor.execute(query,{"postal":postal})
    run_time = time.process_time() - t1

    #print to check
    connection.commit()
    return run_time

def uniformed(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index=FALSE; ')
    ordersnew = '''
    CREATE TABLE "OrdersNew" ("order_id"	TEXT,"customer_id" TEXT);
    INSERT INTO OrdersNew
    SELECT order_id, customer_id
    FROM Orders;
    ALTER TABLE Orders RENAME TO OrdersOriginal;
    ALTER TABLE OrdersNew RENAME TO Orders;
    '''
    cursor.executescript(ordersnew)
    
     
    Customersnew = '''
    CREATE TABLE "CustomersNew" ("customer_id" TEXT, "customer_postal_code" INTEGER);
    INSERT INTO CustomersNew 
    SELECT customer_id, customer_postal_code
    FROM Customers;
    ALTER TABLE Customers RENAME TO CustomersOriginal;
    ALTER TABLE CustomersNew RENAME TO Customers;
    ''' 
    cursor.executescript(Customersnew)
    connection.commit()
    
    time_=Query3(postal)
    
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOriginal RENAME TO Customers;''')
    cursor.execute(''' DROP TABLE Orders;''')
    cursor.execute('''ALTER TABLE OrdersOriginal RENAME TO Orders;''')
    connection.commit()
    
    return time_*1000
def self_opt(postal):
    global connection, cursor
    cursor.execute('PRAGMA automatic_index=True;')
    connection.commit()
    x = Query3(postal)
    return x*1000

def user_opt(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index = FALSE; ')
    index_ = ''' CREATE INDEX customer_index ON Customers (customer_postal_code, customer_id);
                 CREATE INDEX order_index ON Orders (customer_id, order_id);'''
    cursor.executescript(index_)
    connection.commit()
    x = Query3(postal)
    cursor.execute('''DROP INDEX IF EXISTS c_index;''')
    cursor.execute('''DROP INDEX IF EXISTS p_index;''')
    connection.commit()
    return x*1000
def collectTime():
    runningTimeList = []
    for i in range (50):
        start = time.time()
        Query3()
        end = time.time()
        runningTime = end - start
        runningTimeList.append(runningTime)
    avgTime = sum(runningTimeList)*1000/50
    return avgTime

# Query 1 using smallDB size
def smallDBQuery():
    global connection, cursor
    #uniformed
    db_path = './A3small.db'
    connect(db_path)
    z = []
    cursor.execute('''SELECT C.customer_postal_code
             FROM Customers C
        ''')
    #cursor.execute(q_z)
    row = cursor.fetchall()
    for count in row:
        z.append(str(count[0]))
    time =[]
    for i in range(50):
        time.append(uniformed(random.choice(z)))
    avg = sum(time)/len(time)
    uni.append(avg)
    connection.close()
    #self-optimization
    db_path = './A3small.db'
    connect(db_path)
    self_opt()
    time = []
    for i in range(50):
        time.append(self_opt(random.choice(z)))
    avg = sum(time)/len(time)
    self.append(avg)
    connection.close()

    time = []
    for i in range(50):
        time.append(user_opt(random.choice(z)))
    connection.close()
    avg = sum(time)/len(time)
    user.append(avg)
    connection.close
 
    print(uni)
    print(self)
    print(user)
   
    
    
# Query 1 using smallDB size

def mediumDBQuery():
    #uniformed
    db_path = './A3Medium.db'
    connect(db_path)
    z = []
    q_z = '''SELECT C.customer_postal_code
                 FROM Customers C
        '''
    cursor.execute(q_z)
    row = cursor.fetchall()
    for count in row:
        z.append(str(count[0]))
    time =[]
    for i in range(50):
        time.append(uniformed(random.choice(z)))
    avg = sum(time)/len(time)
    uni.append(avg)
    connection.close()
    #self-optimization
    db_path = './A3Medium.db'
    connect(db_path)
    self_opt()
    time = []
    for i in range(50):
        time.append(self_opt(random.choice(z)))
    avg = sum(time)/len(time)
    self.append(avg)
    connection.close()

    time = []
    for i in range(50):
        time.append(user_opt(random.choice(z)))
    connection.close()
    avg = sum(time)/len(time)
    user.append(avg)
    connection.close
 
    print(uni)
    print(self)
    print(user)
   
# Query 1 using mediumDB size
def largeDBQuery():
    #uniformed
    db_path = './A3Large.db'
    connect(db_path)
    z = []
    q_z = '''SELECT C.customer_postal_code
                 FROM Customers C
        '''
    cursor.execute(q_z)
    row = cursor.fetchall()
    for count in row:
        z.append(str(count[0]))
    time =[]
    for i in range(50):
        time.append(uniformed(random.choice(z)))
    avg = sum(time)/len(time)
    uni.append(avg)
    connection.close()
    #self-optimization
    db_path = './A3Large.db'
    connect(db_path)
    time = []
    for i in range(50):
        time.append(self_opt(random.choice(z)))
    avg = sum(time)/len(time)
    self.append(avg)
    connection.close()

    time = []
    for i in range(50):
        time.append(user_opt(random.choice(z)))
    connection.close()
    avg = sum(time)/len(time)
    user.append(avg)
    connection.close
 
    print(uni)
    print(self)
    print(user)


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
    global connection, cursor

    #smallDBQuery()
    #mediumDBQuery()
    largeDBQuery()
    #call all queries 
    #optimize queries 
    #make a graph


if __name__ == "__main__":
    main()