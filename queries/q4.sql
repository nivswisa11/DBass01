SELECT  CONCAT(customer.first_name, ' ', customer.last_name) as FULL_NAME
FROM customer,rental
WHERE customer.customer_id =rental.customer_id AND rental.rental_date >= '2005-05-01' AND rental.rental_date <= '2005-05-31'
GROUP BY customer.customer_id
HAVING COUNT(*)>=ALL (SELECT COUNT(*)
						FROM rental
						WHERE rental.rental_date >= '2005-05-01' AND rental.rental_date <= '2005-05-31'
						GROUP BY rental.customer_id)