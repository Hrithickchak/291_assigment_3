import csv
import random
import sqlite3
import time

#cursor.execute(' PRAGMA foreign_keys=ON; ')
#read organize shuffle customer sellers order items

def Customer():

    csvread_1 = open("olist_customers_dataset.csv","r")
    reader_1 = csv.reader(csvread_1)

    next(reader_1)
    customerid = [column[0] for column in reader_1]

    csvread_2 = open("olist_customers_dataset.csv","r")
    reader_2 = csv.reader(csvread_2)
    next(reader_2)
    postal = [column[2] for column in reader_2]

    combine = []
    for i in range(len(postal)):
        combine.append([customerid[i],postal[i]])
    
    random.shuffle(combine)
    return combine

def Orders():
    csvread_x = open("olist_orders_dataset.csv","r")
    reader_x = csv.reader(csvread_x)

    next(reader_x)
    order_id = [column[0] for column in reader_x]

    csvread_2= open("olist_orders_dataset.csv","r")
    reader_2 = csv.reader(csvread_2)
    next(reader_2)
    customer_id = [column[1] for column in reader_2]

    combine1 = []
    for i in range(len(customer_id)):
        combine1.append([order_id[i],customer_id[i]])
    
    random.shuffle(combine1)
    return combine1
def sellers():
    csvread_y = open("olist_sellers_dataset.csv","r")
    reader_y = csv.reader(csvread_y)

    next(reader_y)
    order_id = [column[0] for column in reader_y]

    csvread_2 = open("olist_sellers_dataset.csv","r")
    reader_2 = csv.reader(csvread_2)
    next(reader_2)
    customer_id = [column[1] for column in reader_2]

    combine2 = []
    for i in range(len(customer_id)):
        combine2.append([order_id[i],customer_id[i]])
    
    random.shuffle(combine2)
    return combine2
def Order_items():
    csvread_z = open("olist_order_items_dataset.csv","r")
    reader_z = csv.reader(csvread_z)

    next(reader_z)
    order_id = [column[0] for column in reader_z]

    csvread_3 = open("olist_order_items_dataset.csv","r")
    reader_3 = csv.reader(csvread_3)
    next(reader_3)
    order_item_id = [column[1] for column in reader_3]
    
    csvread_4 = open("olist_order_items_dataset.csv","r")
    reader_4 = csv.reader(csvread_4)
    next(reader_4)
    product_id = [column[2] for column in reader_4]
    
    csvread_5 = open("olist_order_items_dataset.csv","r")
    reader_5 = csv.reader(csvread_5)
    next(reader_5)
    seller_id = [column[3] for column in reader_5]
    combine3 = []
    for i in range(len(order_id)):
        combine3.append([order_id[i],order_item_id[i],product_id[i],seller_id[i]])
    
    random.shuffle(combine3)
    return combine3
def smallDB(customer,order,seller,items):
    conn = sqlite3.connect('A3Small.db')
    c=conn.cursor()
    #customers
    c.execute('''DROP TABLE IF EXISTS Customers''')
    c.execute('''CREATE TABLE Customers (
                    "customer_id" TEXT,
                    "customer_postal_code" INTEGER,
                    PRIMARY KEY("customer_id")
                    );
        '''
    )
    for i in range (10000):
        c.execute('''INSERT INTO Customers(customer_id, customer_postal_code)
                        VALUES(?,?);''',customer[i])
    #order
    c.execute('''DROP TABLE IF EXISTS Orders''')
    c.execute('''CREATE TABLE Orders (
                    "order_id" TEXT,
                    "customer_id" TEXT,
                    PRIMARY KEY("order_id"),
                    FOREIGN KEY("customer_id") REFERENCES "Customers"("custoemr_id")
                    );
        '''
    )
    for i in range (10000):
        c.execute('''INSERT INTO Orders(order_id, customer_id)
                        VALUES(?,?);''',order[i])
#sellers
    c.execute('''DROP TABLE IF EXISTS Sellers''')
    c.execute('''CREATE TABLE Sellers (
                    seller_id TEXT,
                    seller_postal_code INTEGER,
                    PRIMARY KEY("seller_id")
                    );
        ''')
    
    for i in range (500):
        c.execute('''INSERT INTO Sellers(seller_id, seller_postal_code)
                        VALUES(?,?);''',seller[i])
     #Order_items
    c.execute('''DROP TABLE IF EXISTS Order_items''')
    c.execute('''CREATE TABLE Order_items (
                    order_id TEXT,
                    order_item_id INTEGER,
                    product_id TEXT,
                    seller_id TEXT,
                    PRIMARY KEY("order_id","order_item_id","product_id","seller_id"),
	                FOREIGN KEY("seller_id") REFERENCES "Sellers"("seller_id"),
	                FOREIGN KEY("order_id") REFERENCES "Orders"("order_id")
                    );
        '''
    )
    for i in range (2000):
        c.execute('''INSERT INTO Order_items(order_id,order_item_id,product_id,seller_id)
                        VALUES(?,?,?,?);''',items[i])
    conn.commit()
    conn.close()
smallDB(Customer(),Orders(),sellers(),Order_items())