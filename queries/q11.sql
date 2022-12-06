SELECT MAX(b.total_earnings - a.total_earnings) AS earning_difference, a.store
FROM payment, (SELECT ROW_NUMBER() OVER (ORDER BY payment.staff_id) row_num1, 
SUM(payment.amount) AS total_earnings, YEAR(payment.payment_date) AS year, MONTH(payment.payment_date) AS month, payment.staff_id AS store
FROM payment
GROUP BY month, year, payment.staff_id
ORDER BY payment.staff_id, year, month) AS a, 

(SELECT ROW_NUMBER() OVER (ORDER BY payment.staff_id) row_num2, 
SUM(payment.amount) AS total_earnings, YEAR(payment.payment_date) AS year, MONTH(payment.payment_date) AS month, payment.staff_id AS store
FROM payment
GROUP BY month, year, payment.staff_id
ORDER BY payment.staff_id, year, month) AS b
WHERE row_num1 + 1 = row_num2 AND a.month + 1 = b.month AND a.store = payment.staff_id
GROUP BY a.store
ORDER BY earning_difference DESC
LIMIT 1