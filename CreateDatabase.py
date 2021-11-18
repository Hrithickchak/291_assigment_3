import csv
import random
import sqlite3
import time

"""
This function will create different amount of data list
"""
def differentDB(amount):
    #open upc_corpus.csv, and read part_number, needs_part to alist
    csvread_1 = open("upc_corpus.csv","r")
    
    reader_1 = csv.reader(csvread_1)
    #skip the title line
    next(reader_1)
    alist = [column[0] for column in reader_1]
    alist = list(set(alist))

    #shuffle alist and append top non-null elements to the partnumber_list
    random.shuffle(alist)
    partnumber_list = []
    for i in alist:
        
        if i.isdigit() and len(i)<=18:     
            partnumber_list.append(int(i))
        
        if len(partnumber_list) == amount:
            break

    #shuffle alist and append top non-null elements to the needspart_list
    random.shuffle(alist)
    needspart_list = []
    for i in alist:
        if i.isdigit() and len(i)<=18:
            needspart_list.append(int(i))

        if len(needspart_list) == amount:
            break


    #open data.csv
    csvread_2 = open("data.csv","r")
    reader_2 = csv.reader(csvread_2)
    #skip the title line
    next(reader_2)
    clist = [row[1] for row in reader_2]

    random.shuffle(clist)
    #get madein_list
    madein_list = []
    for i in range(amount):
        madein = random.choice(clist)
        madein_list.append(madein)

    #get part_price list
    partprice_list = []
    for i in range(amount):
        partprice = random.randint(1,100)
        partprice_list.append(partprice)

    #put 4 list in 1 big list
    finallist = [list(item) for item in zip(partnumber_list,partprice_list,needspart_list,madein_list)]

    return finallist

"""
This function create 100 element database
"""
def create100(dealedList):
    conn = sqlite3.connect('A4v100.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS Parts''')

    c.execute(''' CREATE TABLE Parts (
                        partNumber INTEGER,
                        partPrice INTEGER,
                        needsPart INTEGER,
                        madeIn TEXT,
                        PRIMARY KEY(partNumber));''')

    for i in range(len(dealedList)):
        c.execute('''INSERT INTO Parts(partNumber, partPrice, needsPart, madeIn)
                            VALUES (?, ?, ?, ?);''' ,dealedList[i])
    conn.commit()
    conn.close()

"""
This function create 1k element database
"""
def create1k(dealedList):
    conn = sqlite3.connect('A4v1k.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS Parts''')

    c.execute(''' CREATE TABLE Parts (
                        partNumber INTEGER,
                        partPrice INTEGER,
                        needsPart INTEGER,
                        madeIn TEXT,
                        PRIMARY KEY(partNumber));''')

    for i in range(len(dealedList)):
        c.execute('''INSERT INTO Parts(partNumber, partPrice, needsPart, madeIn)
                            VALUES (?, ?, ?, ?);''' ,dealedList[i])
    conn.commit()
    conn.close()

"""
This function create 10k element database
"""
def create10k(dealedList):
    conn = sqlite3.connect('A4v10k.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS Parts''')

    c.execute(''' CREATE TABLE Parts (
                        partNumber INTEGER,
                        partPrice INTEGER,
                        needsPart INTEGER,
                        madeIn TEXT,
                        PRIMARY KEY(partNumber));''')

    for i in range(len(dealedList)):
        c.execute('''INSERT INTO Parts(partNumber, partPrice, needsPart, madeIn)
                            VALUES (?, ?, ?, ?);''' ,dealedList[i])
    conn.commit()
    conn.close()

"""
This function create 100k element database
"""
def create100k(dealedList):
    conn = sqlite3.connect('A4v100k.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS Parts''')

    c.execute(''' CREATE TABLE Parts (
                        partNumber INTEGER,
                        partPrice INTEGER,
                        needsPart INTEGER,
                        madeIn TEXT,
                        PRIMARY KEY(partNumber));''')

    for i in range(len(dealedList)):
        c.execute('''INSERT INTO Parts(partNumber, partPrice, needsPart, madeIn)
                            VALUES (?, ?, ?, ?);''' ,dealedList[i])
    conn.commit()
    conn.close()

"""
This function create 1M element database
"""
def create1M(dealedList):
    conn = sqlite3.connect('A4v1M.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS Parts''')

    c.execute(''' CREATE TABLE Parts (
                        partNumber INTEGER,
                        partPrice INTEGER,
                        needsPart INTEGER,
                        madeIn TEXT,
                        PRIMARY KEY(partNumber));''')

    for i in range(len(dealedList)):
        c.execute('''INSERT INTO Parts(partNumber, partPrice, needsPart, madeIn)
                            VALUES (?, ?, ?, ?);''' ,dealedList[i])
    conn.commit()
    conn.close()

def main():
    
    print("Start create 100")
    #create 100 element database
    List100 = differentDB(100)
    create100(List100)

    print("Start create 1k")
    #create 1000 element database
    List1k = differentDB(1000)
    create1k(List1k)

    print("Start create 10k")
    #create 10000 element database
    List10k = differentDB(10000)
    create10k(List10k)

    print("Start create 100k")
    #create 100000 element database
    List100k = differentDB(100000)
    create100k(List100k)
    
    print("Start create 1M")
    #create 1000000element database
    List1M = differentDB(1000000)
    create1M(List1M)

main()
