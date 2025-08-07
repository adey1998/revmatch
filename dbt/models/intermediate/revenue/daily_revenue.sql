-- DEFINE USAGE TABLE
WITH usage AS (
    SELECT
        tenant_id,
        event_type,
        DATE_TRUNC(DATE(event_timestamp), DAY) AS event_date
    FROM {{ ref('stg_usage_events') }}
    WHERE event_type = 'subscription_billed'
),

-- DEFINE BILLING TABLE
billing AS (
    SELECT
        tenant_id,
        amount,
        DATE_TRUNC(DATE(billing_time), DAY) AS billing_date
    FROM {{ ref('stg_billing_records') }}
),

-- JOINED USAGE + BILLING ON TENANT_ID + DATE
joined AS (
    SELECT
        u.tenant_id,
        u.event_date,
        b.amount
    FROM usage u
    LEFT JOIN billing b
        ON u.tenant_id = b.tenant_id
        AND u.event_date = b.billing_date
)

-- FINAL AGGREGATION: OUR DAILY_REVENUE MODEL
SELECT
    tenant_id,
    event_date,
    COALESCE(SUM(amount), 0) AS daily_revenue
FROM joined
GROUP BY tenant_id, event_date
ORDER BY event_date
