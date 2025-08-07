-- CORE MODEL: TENANT TOTALS BASED ON DAILY REVENUE
WITH daily_rev_data AS (
    SELECT
        CAST(d.tenant_id AS STRING) AS tenant_id,
        CAST(d.event_date AS DATE) AS event_date,
        CAST(d.daily_revenue AS FLOAT64) AS daily_revenue
    FROM {{ ref('daily_revenue') }} d
)

SELECT
    tenant_id,
    COUNT(DISTINCT event_date) AS active_days,
    SUM(daily_revenue) AS total_revenue,
    AVG(daily_revenue) AS avg_daily_revenue
FROM daily_rev_data
GROUP BY tenant_id
