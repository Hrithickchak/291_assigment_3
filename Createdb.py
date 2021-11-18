import csv
import random
import sqlite3
import time

#cursor.execute(' PRAGMA foreign_keys=ON; ')

#to do list
# create each db A3Small.db, A3Medium.db and A3Large.db
# organize each by cardinality 

#read organize shuffle customer sellers order items
def smalldb():
    csvread_1 = open("olist_customers_dataset.csv","r")
    reader_1 = csv.reader(csvread_1)

    next(reader_1)
    alist = [column[0] for column in reader_1]
    alist = list(set(alist))

    #shuffle alist and append top non-null elements to customers
    random.shuffle(alist)
    print(alist)
smalldb()


#olist_sellers_dataset.csv
#olist_orders_dataset.csv
#olist_order_items_dataset.csv
"""def mediumdb():

    csvread_1 = open(".csv","r")
def largedb():
 csvread_1 = open(".csv","r")
"""
