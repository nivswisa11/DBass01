SELECT film_id, title
FROM film
WHERE film.length < 90 AND (film.rating = 'PG' OR film.rating = 'G') 