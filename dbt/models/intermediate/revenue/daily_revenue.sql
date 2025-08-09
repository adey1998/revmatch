-- DAILY_REVENUE: include all tenant/date activity; avoid duplicate sums

-- 1) Usage days (you can keep this filter now that you emit it)
WITH usage_days AS (
  SELECT
    CAST(tenant_id AS STRING) AS tenant_id,
    DATE_TRUNC(DATE(event_timestamp), DAY) AS event_date
  FROM {{ ref('stg_usage_events') }}
  WHERE event_type = 'subscription_billed'
  GROUP BY 1, 2
),

-- 2) Billing aggregated per tenant/day (pre-aggregate to avoid double-counting)
billing_daily AS (
  SELECT
    CAST(tenant_id AS STRING) AS tenant_id,
    DATE_TRUNC(DATE(billing_time), DAY) AS event_date,
    SUM(CAST(amount AS FLOAT64)) AS daily_revenue
  FROM {{ ref('stg_billing_records') }}
  GROUP BY 1, 2
),

-- 3) All activity days (usage OR billing)
all_days AS (
  SELECT tenant_id, event_date FROM usage_days
  UNION DISTINCT
  SELECT tenant_id, event_date FROM billing_daily
)

-- 4) Final: every tenant/date with billed amount (0 if none)
SELECT
  a.tenant_id,
  a.event_date,
  COALESCE(b.daily_revenue, 0) AS daily_revenue
FROM all_days a
LEFT JOIN billing_daily b
  ON a.tenant_id = b.tenant_id
 AND a.event_date = b.event_date
ORDER BY a.tenant_id, a.event_date
