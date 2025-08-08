{{ config(materialized='view') }}

-- Purpose:
-- Prepare raw billing records for downstream transformations by:
-- 1. Renaming columns to snake_case for consistency.
-- 2. Standardizing column names for clarity:
--    - tenant_id → tenant_id
--    - amount → amount
--    - billed_at → billing_time


select
    tenant_id,
    amount        as amount,
    billed_at     as billing_time
from {{ source('revmatch', 'billing_records') }}
