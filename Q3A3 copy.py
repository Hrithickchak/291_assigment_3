import time
import matplotlib.pyplot as plt
import sqlite3
import random
uni=[]
self=[]
user=[] 
connection = None
cursor = None
postal = []

def Query3(postal):
    global connection, cursor
    
    connection.commit()
    
    Query3 = ''' SELECT COUNT(*), AVG(o_s.size)
                FROM Orders, Customers, ( SELECT order_id as oid, COUNT(DISTINCT order_item_id) as size FROM Order_items O GROUP BY O.order_id )as o_s
                WHERE Orders.customer_id = Customers.customer_id AND Customers.customer_postal_code=:postal AND o_s.oid=Orders.order_id
            '''
    t = time.process_time()
    cursor.execute(Query3,{"postal":postal})
    elapsed_time = time.process_time() - t
    connection.commit()
    
    return elapsed_time

def uniformed(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index=FALSE; ')
    ordersnew = ''' CREATE TABLE "OrdersNew" ("order_id"	TEXT,"customer_id" TEXT); INSERT INTO OrdersNew
    SELECT order_id, customer_id FROM Orders;
    ALTER TABLE Orders RENAME TO OrdersOriginal; ALTER TABLE OrdersNew RENAME TO Orders;
    '''
    cursor.executescript(ordersnew)
    Customersnew = ''' CREATE TABLE "CustomersNew" ("customer_id" TEXT, "customer_postal_code" INTEGER); INSERT INTO CustomersNew 
    SELECT customer_id, customer_postal_code 
    FROM Customers;
    ALTER TABLE Customers RENAME TO CustomersOriginal;
    ALTER TABLE CustomersNew RENAME TO Customers; ''' 
    cursor.executescript(Customersnew)
    connection.commit()
    x=Query3(postal)
    cursor.execute('''DROP TABLE Customers;''')
    cursor.execute('''ALTER TABLE CustomersOriginal RENAME TO Customers;''')
    cursor.execute(''' DROP TABLE Orders;''')
    cursor.execute('''ALTER TABLE OrdersOriginal RENAME TO Orders;''')
    connection.commit()
    y = x*1000
    return y

def self_opt(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index = TRUE; ')
    connection.commit()
    x=Query3(postal)
    y = x * 1000
    return y

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


def plot():
    labels=["small","medium","large"]
    fig,ax=plt.subplots()
    ax.bar(labels,uni,0.5,label='uniformed')
    ax.bar(labels,self,0.5,bottom=uni,label='self-optimization')
    ax.bar(labels,user,0.5,bottom = list(map(lambda x,y: x+y, uni, self)) ,label='user-optimization')
    ax.set_ylabel('time (ms)')
    ax.set_title('Query 3 (runtime in ms)')
    ax.legend()
    path = './{}chart.png'.format('Q3A3')
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    plt.close()

def user_opt(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index = FALSE; ')
   
    index_ = ''' CREATE INDEX customer_index ON Customers (customer_postal_code, customer_id);
                 CREATE INDEX order_index ON Orders (customer_id, order_id);'''
    cursor.executescript(index_)
    connection.commit()
    x=Query3(postal)
    cursor.execute('''DROP INDEX customer_index''')
    cursor.execute('''DROP INDEX order_index''')
    connection.commit()
    y = x * 1000
    return y  

def make_optimization_lists(p):
    count=[]
    postal=[]
    connect(p)
    query='''SELECT C.customer_postal_code
                FROM Customers C
    '''
    cursor.execute(query)
    rows=cursor.fetchall()
    for each in rows:
        postal.append(str(each[0]))

    for i in range(50):
        count.append(uniformed(random.choice(postal)))
    
    avg_time=sum(count)/len(count)
    uni.append(avg_time)
    connection.close()
    connect(p)
    
    count=[]
    for i in range(50):
        count.append(self_opt(random.choice(postal)))

    avg_time=sum(count)/len(count)
    self.append(avg_time)

    connection.close()
    connect(p)


    count=[]
    for i in range(50):
        count.append(user_opt(random.choice(postal)))

    avg_time=sum(count)/len(count)
    user.append(avg_time)
        
    connection.close()
        
    
def main():
    global connection, cursor
    p = './A3small.db'
    make_optimization_lists(p)
    q = './A3Medium.db'
    make_optimization_lists(q)
    r = './A3Large.db'
    make_optimization_lists(r)
    
    plot()


if __name__ == "__main__":
    main()
