import sqlite3
# matplotlib.pyplot will allow us to create visualizations of our results
import matplotlib.pyplot as plt
import numpy as np 

#Given a random customer_postal_code from Customers, 
#find how many orders have been placed by customers 
#who have that customer_postal_code.




'''
SELECT COUNT(order_id)
FROM Customers C ,Orders O
WHERE
C.customer_id = O.customer_id AND C.customer_postal_code = 4777



query = 
    SELECT NEIGHBOURHOOD, CAST (SUM(FEMALE) AS REAL)/SUM(MALE) 
    FROM Census2012 
    WHERE( FEMALE + MALE)>:4777
    GROUP BY NEIGHBOURHOOD

    t_flag = float(input('Include threshold: ')) 
    # execute query with provided flags
    cursor.execute(query, {'tflag': t_flag })

'''



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
        elif query_selection == '2':
            mediumDBQuery()
        elif query_selection == '3':
            largeDBQuery()
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