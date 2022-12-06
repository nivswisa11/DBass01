SELECT customer.first_name, customer.last_name
FROM customer
WHERE customer.first_name NOT IN 
(SELECT actor.first_name
FROM actor) 

UNION

SELECT actor.first_name, actor.last_name
FROM actor
WHERE actor.first_name NOT IN 
(SELECT customer.first_name
FROM customer) 

