with source as (
    select * from {{ ref('usage_events') }}
)

select
    tenantId as tenant_id,
    event as event_type,
    timestamp as event_timestamp
from source
