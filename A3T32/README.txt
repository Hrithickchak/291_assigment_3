Group 32
ccid:
    ssekowsk
    hrithick
    lantian
    kazihasi
Names:
    Sebastian Sekowski
    Hrithick Chakraborty
    Lantian Zhao
    Kazi Hasin Sohail
Resource:
    Stack Overflow
    https://www.tutorialspoint.com/
    https://docs.python.org/

"We declare that we did not collaborate with anyone outside our own group in this assignment" 

Reasoning for choices made for each query under the “User Optimized” Scenario

Query #1: 

We executed the following SQL query:

SELECT COUNT(order_id) 
    FROM Customers C, Orders O 
    WHERE C.customer_id = O.customer_id AND
    customer_postal_code = (SELECT C.customer_postal_code 
    FROM Customers C ORDER BY random() LIMIT 1);

We created idicies for postal code and customer id in query 1 for User Optimized to help the tables search results more quickly 

Query #2: 

We executed the following SQL query:

SELECT COUNT(*), AVG(OS.size) FROM Orders O, Customers C, ordersize OS WHERE O.customer_id = C.customer_id
                AND C.customer_postal_code=:postal AND OS.oid=O.order_id

We created idicies for customer_postal code in query 2 for User Optimized to help the tables search results more quickly 

Query #3: 

We executed the following SQL query:

SELECT COUNT(*), AVG(OS.size)
                FROM Orders O, Customers C, ( SELECT order_id as oid, COUNT(DISTINCT order_item_id) as size FROM Order_items O GROUP BY O.order_id )as OS
                WHERE O.customer_id = C.customer_id
                AND C.customer_postal_code=:postal
                AND OS.oid=O.order_id

We created idicies for postal code and customer id in query 3 for User Optimized to help the tables search results more quickly 

Query #4: 

We executed the following SQL query:

SELECT count(DISTINCT s.seller_postal_code)  
        FROM Order_items i, Sellers s 
        WHERE i.order_id = (SELECT o_i.order_id FROM  Order_items o_i ORDER BY random() LIMIT 1)
        AND i.seller_id = s.seller_id

We created idicies for postal code and order id in query 4 for User Optimized to help the tables search results more quickly

