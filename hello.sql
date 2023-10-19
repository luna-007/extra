USE sql_store;

SELECT * 
FROM customers 
-- WHERE customer_id = 1
ORDER BY first_name

SELECT  
    first_name, 
    last_name, 
    points ,
    points + 10 * 10 AS new_points
    FROM customers 
        ORDER BY points DESC;

SELECT 
    state 
    FROM customers;

use sql_inventory;

SELECT 
    name, 
    unit_price,
    unit_price * 1.1 as new_price
        FROM products;

USE sql_store;

SELECT * FROM customers WHERE birth_date < '1990-01-01' ORDER BY birth_date ASC;

SELECT * FROM customers WHERE birth_date > '1980-01-01' AND points > 1500 ORDER BY points;

SELECT * FROM order_items WHERE order_Id = 6 AND (unit_price * quantity) > 30 ORDER BY (unit_price * quantity) ASC;

SELECT * FROM order_items

SELECT * from customers WHERE state IN ('VA', 'FL', 'GA')  ORDER BY points ASC;

SELECT DISTINCT state FROM customers;

SELECT * FROM products WHERE quantity_in_stock IN (49, 38, 72)

