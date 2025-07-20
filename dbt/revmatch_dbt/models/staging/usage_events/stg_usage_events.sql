-- Purpose:
-- Prepare raw usage events for downstream transformations by:
-- 1. Renaming columns to snake_case for consistency.
-- 2. Standardizing column names for clarity:
--    - tenantId → tenant_id
--    - event → event_type
--    - timestamp → event_timestamp
-- This model maintains row-level granularity and avoids applying any business logic.
-- It serves as a clean, reliable source for core models.


{{ config(materialized='view') }}

SELECT
    tenantId    AS tenant_id,
    event       AS event_type,
    timestamp   AS event_timestamp
FROM {{ source('revmatch_dataset', 'usage_events') }}
