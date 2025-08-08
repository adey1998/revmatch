{{ config(materialized='view') }}

-- Purpose:
-- Prepare raw usage events for downstream transformations by:
-- 1. Renaming columns to snake_case for consistency.
-- 2. Standardizing column names for clarity:
--    - tenant_id → tenant_id
--    - event → event_type
--    - timestamp → event_timestamp


SELECT
    tenant_id,
    event       AS event_type,
    timestamp   AS event_timestamp
FROM {{ source('revmatch', 'usage_events') }}
