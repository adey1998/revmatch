{{ config(materialized='view') }}

-- Purpose:
-- Prepare raw billing records for downstream transformations by:
-- 1. Renaming columns to snake_case for consistency.
-- 2. Standardizing column names for clarity:
--    - tenant_id → tenant_id
--    - amount → amount
--    - billed_at → billing_time


SELECT
    tenant_id,
    amount,
    billing_time
FROM {{ source('revmatch', 'billing_records') }}
