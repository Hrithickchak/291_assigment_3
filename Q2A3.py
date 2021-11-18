import sqlite3
# matplotlib.pyplot will allow us to create visualizations of our results
import matplotlib.pyplot as plt
import numpy as np

#from Createdb import smallDB 



def smallDBQuery():

    global connection, cursor

    cursor.excute('''CREATE VIEW OrderSize(oid, size)
    AS SELECT order_id, order_item_id    
	FROM Orders o, Order_items i
     ''')
    #find a way to print 
    s = cursor.fetchone()
    print(s)



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
    # we will hard code the database name, could also get from user
    db_path = './A3small.db'
    #open multiple db paths? medium and large
    # create connection using function defined above
    connect(db_path)
    # loop program until user chooses to exit
    while(True):
        # prompt user to selet query
        print('\nFind how many orders have been placed by customers who have that customer_postal_code.')
        #Given a random customer_postal_code from Customers, 
        print('1. Run with smallDB')
        print('2. Run with mediumDB')
        print('3. Run with largeDB')
        print('4. Exit program')
        query_selection = input('Selection: ')
        # input function will return string so compare to strings
        if query_selection == '1':
            smallDBQuery()
       # elif query_selection == '2':
            #mediumDBQuery()
        #elif query_selection == '3':
            #largeDBQuery()
        # if user selects 3 break program while loop and exit program
        elif query_selection == '4':
            print('Goodbye :)')
            break
        # if user enters anything but 1, 2, or 3 prompt for valid input
        else:
            print("\nInvalid input!\nSelection must be 1, 2, 3, 4")
    
    # close connection before exiting
    connection.close()
  
# run main method when program starts
if __name__ == "__main__":
    main()