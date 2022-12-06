SELECT t1.renter_name, t1.film, t1.rental_dur
FROM 
(SELECT CONCAT(first_name, " ", last_name) AS renter_name, film.title as film, weekRental.rental_duration as rental_dur
FROM customer, inventory, film,
	(SELECT (DATEDIFF(return_date, rental_date)/7) AS rental_duration, inventory_id, customer_id
	FROM rental) AS weekRental
WHERE weekRental.inventory_id = inventory.inventory_id AND inventory.film_id = film.film_id AND weekRental.customer_id = customer.customer_id) AS t1
WHERE t1.rental_dur = 
(SELECT MAX((DATEDIFF(return_date, rental_date)/7)) AS rental_duration
FROM rental)