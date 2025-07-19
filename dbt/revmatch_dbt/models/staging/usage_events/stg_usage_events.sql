{{ config(materialized='view') }}

select
    tenantId    as tenant_id,
    event       as event_type,
    timestamp   as event_timestamp
from {{ source('revmatch_dataset', 'usage_events') }}
