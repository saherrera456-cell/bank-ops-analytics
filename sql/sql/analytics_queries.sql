-- KPI 1: Volumen diario por status
SELECT
  date_trunc('day', tx_timestamp) AS day,
  status,
  COUNT(*) AS tx_count,
  SUM(amount) AS amount_sum
FROM transactions
GROUP BY 1,2
ORDER BY 1,2;

-- KPI 2: Aprobación por canal
SELECT
  channel,
  100.0 * SUM(CASE WHEN status='APPROVED' THEN 1 ELSE 0 END) / COUNT(*) AS approval_rate
FROM transactions
GROUP BY 1
ORDER BY 2 DESC;

-- KPI 3: Ticket promedio por país
SELECT
  country,
  AVG(amount) AS avg_ticket
FROM transactions
GROUP BY 1
ORDER BY 2 DESC;
