SELECT AVG(film.length) AS avg_length, category.name AS category
FROM film, film_category AS fc, category
WHERE film.film_id = fc.film_id AND category.category_id = fc.category_id
GROUP BY category.name