{{ config(materialized='view') }}

select
    tenantId        as tenant_id,
    billedEvents    as billed_events,
    amountBilled    as amount,
    timestamp       as billing_time
from {{ source('revmatch_dataset', 'billing_records') }}
