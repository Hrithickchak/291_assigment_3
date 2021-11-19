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
                WHERE Orders.customer_id = Customers.customer_id
                AND Customers.customer_postal_code=:postal
                AND o_s.oid=Orders.order_id
            '''
    t = time.process_time()
    cursor.execute(Query3,{"postal":postal})
    elapsed_time = time.process_time() - t
    connection.commit()
    
    return elapsed_time

def uninformed(postal):
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

def self_optimized(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index = TRUE; ')
    connection.commit()
    time_=Query3(postal)
    return time_*1000


def user_optimized(postal):
    global connection, cursor
    cursor.execute(' PRAGMA automatic_index = FALSE; ')
   
    index_ = ''' CREATE INDEX customer_index ON Customers (customer_postal_code, customer_id);
                 CREATE INDEX order_index ON Orders (customer_id, order_id);'''
    cursor.executescript(index_)
    connection.commit()
    time_=Query3(postal)
    cursor.execute('''DROP INDEX customer_index''')
    cursor.execute('''DROP INDEX order_index''')
    connection.commit()
    return time_*1000
    
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

def make_optimization_lists(p):
    times=[]
    postal=[]
    connect(p)
    query='''SELECT C.customer_postal_code
                FROM Customers C
    '''
    cursor.execute(query)
    rows=cursor.fetchall()
    for each in rows:
        postal.append(str(each[0]))

    
    for i in range(50): #uninformed scenario
        times.append(uninformed(random.choice(postal)))
    
    avg_time=sum(times)/len(times)
    uni.append(avg_time)
    
    connection.close()
    connect(p)
    
    times=[]
    for i in range(50): #selfoptimized scenario
        #use random function to pick random postal code
        times.append(self_optimized(random.choice(postal)))
        #times append isnt unique 
    avg_time=sum(times)/len(times)
    self.append(avg_time)

    connection.close()
    connect(p)


    times=[]
    for i in range(50):
        times.append(user_optimized(random.choice(postal)))

    avg_time=sum(times)/len(times)
    user.append(avg_time)
        
    connection.close()
        
    
def main():
    global connection, cursor

    paths=['./A3small.db', './A3Medium.db', './A3Large.db']
    p = './A3small.db'
    make_optimization_lists(p)
    q = './A3Medium.db'
    
    make_optimization_lists(q)
    r = './A3Large.db'
    make_optimization_lists(r)
    
    
    plot(uni, self, user)
    
def plot(uni,self,user):
    
    labels=["small","medium","large"]
    fig,ax=plt.subplots()
    ax.bar(labels,uni,0.5,label='uniformed')
    ax.bar(labels,self,0.5,bottom=uni,label='self-optimization')
    ax.bar(labels,user,0.5,bottom = list(map(lambda x,y: x+y, uni, self)) ,label='user-optimization')
    
    width = 0.5
    uninformed_results=[]
    uninformed_results=uni
    self_optimized_results=[]
    self_optimized_results=self
    user_optimized_results=[]
    user_optimized_results=user
    last_sum=[]
    for i in range(3):
        last_sum.append(uninformed_results[i] + self_optimized_results[i])
        

    fig, ax = plt.subplots()
    
    ax.bar(labels, uninformed_results, width,  label='Uninformed')
    ax.bar(labels, self_optimized_results, width, bottom=uninformed_results,
    label='Self-Optimized')
    ax.bar(labels, user_optimized_results, width, bottom=last_sum,
    label='User-Optimized')
    ax.set_title('Query 3 (runtime in ms)')
    ax.legend()
    
    path = './{}chart.png'.format('Q3A3')
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    
    
    # close figure so it doesn't display
    plt.close()
    return
    
# run main method when program starts
if __name__ == "__main__":
    main()
