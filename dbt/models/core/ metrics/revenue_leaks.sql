{{ config(materialized='table') }}

-- MODEL: revenue_leaks
-- PURPOSE: Identify revenue leakage by comparing
--          expected vs actual billed revenue per tenant
-- BUSINESS IMPACT: Highlights underbilling or overbilling

-- 1. CALCULATE EXPECTED REVENUE FROM USAGE
WITH usage_pricing AS (
    SELECT
        tenant_id,
        -- Count subscription billing events and apply pricing logic
        COUNTIF(event_type = 'subscription_billed') * 100 AS expected_bill
    FROM {{ ref('stg_usage_events') }}
    GROUP BY tenant_id
),

-- 2. CALCULATE ACTUAL REVENUE FROM BILLING RECORDS
billing_totals AS (
    SELECT
        tenant_id,
        COALESCE(SUM(amount), 0) AS actual_bill
    FROM {{ ref('stg_billing_records') }}
    GROUP BY tenant_id
),

-- 3. JOIN USAGE AND BILLING TO IDENTIFY DISCREPANCIES
joined AS (
    SELECT
        u.tenant_id,
        u.expected_bill,
        b.actual_bill,
        (u.expected_bill - b.actual_bill) AS leak_amount,
        CASE
            WHEN (u.expected_bill - b.actual_bill) > 0 THEN 'UNDERBILLED'
            WHEN (u.expected_bill - b.actual_bill) < 0 THEN 'OVERBILLED'
            ELSE 'ACCURATE'
        END AS status
    FROM usage_pricing u
    LEFT JOIN billing_totals b
        ON u.tenant_id = b.tenant_id
)

-- 4. FINAL OUTPUT: SORT TENANTS BY LEAK
SELECT *
FROM joined
ORDER BY leak_amount DESC
