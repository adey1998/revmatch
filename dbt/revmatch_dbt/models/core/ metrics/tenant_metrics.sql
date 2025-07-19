with daily_revenue as (
  select * from {{ ref('daily_revenue') }}
),

tenant_totals as (
  select
    tenant_id,
    count(distinct event_date) as active_days,
    sum(daily_revenue) as total_revenue,
    avg(daily_revenue) as avg_daily_revenue
  from daily_revenue
  group by tenant_id
)

select * from tenant_totals
