-- Purpose:
-- Prepare raw billing records for downstream transformations by:
-- 1. Renaming columns to snake_case for consistency.
-- 2. Standardizing column names for clarity:
--    - tenantId → tenant_id
--    - billedEvents → billed_events
--    - amountBilled → amount
--    - timestamp → billing_time
-- This model maintains row-level granularity and avoids applying any business logic.
-- It serves as a clean, reliable source for core models.


{{ config(materialized='view') }}

SELECT
    tenantId        AS tenant_id,
    billedEvents    AS billed_events,
    amountBilled    AS amount,
    timestamp       AS billing_time
FROM {{ source('revmatch_dataset', 'billing_records') }}
