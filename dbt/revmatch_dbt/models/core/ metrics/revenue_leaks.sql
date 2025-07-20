{{ config(materialized='table') }}

-- 1. CALCULATE EXPECTED REVENUE FROM USAGE
WITH usage_pricing AS (
    SELECT
        tenant_id,
        COUNTIF(event_type = 'subscription_billed') * 100 AS expected_bill
    FROM {{ ref('stg_usage_events') }}
    GROUP BY tenant_id
)