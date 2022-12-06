SELECT first_name, last_name
FROM actor, film_actor AS fa
WHERE actor.actor_id = fa.actor_id
GROUP BY fa.actor_id
HAVING(SELECT AVG(movie_average)
	FROM(SELECT COUNT(fa.actor_id) AS movie_average
	FROM film_actor AS fa
	GROUP BY fa.actor_id) AS movieAvg) + 10 <= COUNT(fa.actor_id)
ORDER BY first_name, last_name