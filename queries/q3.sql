SELECT f.title, ft.title
FROM film AS f, film_text AS ft
WHERE f.film_id = ft.film_id AND f.title != ft.title
ORDER BY f.title