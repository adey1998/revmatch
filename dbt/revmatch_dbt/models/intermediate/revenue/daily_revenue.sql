-- define usage table
with usage as (
    select
        tenant_id,
        event_type,
        date_trunc('day', event_timestamp) as event_date
    from {{ ref('stg_usage_events') }}
    where event_type = 'subscription_billed'
),

-- define billing table
billing as (
    select
        tenant_id,
        amount,
        date_trunc('day', billing_time) as billing_date
    from {{ ref('stg_billing_records') }}
),

-- joined usage + billing on tenant_id + date
joined as (
    select
        u.tenant_id,
        u.event_date,
        b.amount
    from usage u
    left join billing b
        on u.tenant_id = b.tenant_id
        and u.event_date = b.billing_date
)

-- Final aggregation: our daily_revenue model
select
    tenant_id,
    event_date,
    coalesce(sum(amount), 0) as daily_revenue
from joined
group by tenant_id, event_date
order by event_date