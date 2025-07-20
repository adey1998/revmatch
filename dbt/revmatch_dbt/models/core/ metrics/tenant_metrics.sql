-- CORE MODEL: TENANT TOTALS BASED ON DAILY REVENUE
WITH daily_revenue AS (
    SELECT * FROM {{ ref('daily_revenue') }}
),

tenant_totals AS (
    SELECT
        tenant_id,
        COUNT(DISTINCT event_date) AS active_days,
        SUM(daily_revenue) AS total_revenue,
        AVG(daily_revenue) AS avg_daily_revenue
    FROM daily_revenue
    GROUP BY tenant_id
)

SELECT * FROM tenant_totals
