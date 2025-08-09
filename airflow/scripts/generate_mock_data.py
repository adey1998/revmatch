import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42); Faker.seed(42); np.random.seed(42)

DAYS = 30
PRICE_MAP = {"api_call": 0.10, "report_generation": 0.50, "dashboard_view": 0.05}

TENANTS = [
    # id, usage pattern, billing mode, params
    {"id": "acme_saas",       "pattern": "heavy",  "bill_mode": "under",   "bill_fraction": 0.60},
    {"id": "globex_cloud",    "pattern": "steady", "bill_mode": "over",    "bill_fraction": 0.90, "over_extra_rate": 0.15},
    {"id": "initech_io",      "pattern": "light",  "bill_mode": "accurate","bill_fraction": 1.00},
    {"id": "hooli_enterprise","pattern": "spiky",  "bill_mode": "under",   "bill_fraction": 0.50},
]

EVENT_WEIGHTS_BY_PATTERN = {
    "heavy":  {"api_call": 0.70, "report_generation": 0.20, "dashboard_view": 0.10},
    "steady": {"api_call": 0.50, "report_generation": 0.30, "dashboard_view": 0.20},
    "light":  {"api_call": 0.30, "report_generation": 0.20, "dashboard_view": 0.50},
    "spiky":  {"api_call": 0.60, "report_generation": 0.25, "dashboard_view": 0.15},
}

# average daily usage volumes by pattern
LAMBDA_BY_PATTERN = {
    "heavy":  60,   # ~60 events/day
    "steady": 30,
    "light":  8,
    "spiky":  10,   # most days low, some days huge spikes
}

def random_time_on_day(day_dt):
    # return a datetime on that calendar day
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day_dt.replace(hour=hour, minute=minute, second=second, microsecond=0)

def gen_usage_for_tenant(t):
    tid = t["id"]
    pattern = t["pattern"]
    weights = EVENT_WEIGHTS_BY_PATTERN[pattern]
    lam = LAMBDA_BY_PATTERN[pattern]

    rows = []
    today = datetime.utcnow().replace(microsecond=0)

    for d in range(DAYS):
        day = today - timedelta(days=d)

        # daily volume
        if pattern == "spiky" and random.random() < 0.2:
            n = np.random.poisson(lam * 8)  # occasional spikes
        else:
            n = np.random.poisson(lam)

        # ensure at least some activity on active days
        if n == 0 and random.random() < 0.3:
            n = 1

        # optional: guarantee one subscription_billed per day so your current daily_revenue model (which filters on it) includes this day
        sb_time = random_time_on_day(day)
        rows.append({"tenant_id": tid, "event": "subscription_billed", "timestamp": sb_time.isoformat()})

        # the rest are metered events
        events = list(weights.keys())
        probs  = list(weights.values())
        for _ in range(n):
            et = random.choices(events, probs)[0]
            ts = random_time_on_day(day)
            rows.append({"tenant_id": tid, "event": et, "timestamp": ts.isoformat()})

    return pd.DataFrame(rows)

def gen_billing_for_tenant(usage_df, t):
    billed = usage_df.copy()

    # map amounts for metered events; subscription_billed gets a flat $1.00
    price_map = PRICE_MAP | {"subscription_billed": 1.00}
    billed["amount"] = billed["event"].map(price_map)
    billed["billing_time"] = pd.to_datetime(billed["timestamp"])

    mode = t["bill_mode"]
    frac = t.get("bill_fraction", 1.0)

    if mode == "accurate":
        out = billed
    elif mode == "under":
        out = billed.sample(frac=frac, random_state=42).copy()
    elif mode == "over":
        # bill most usage…
        base = billed.sample(frac=frac, random_state=42).copy()
        # …plus some extra "ghost" charges with no matching usage
        n_extra = int(len(billed) * t.get("over_extra_rate", 0.15))
        extras = []
        if n_extra > 0:
            for _ in range(n_extra):
                et = random.choices(list(PRICE_MAP.keys()), [0.6, 0.25, 0.15])[0]
                ts = fake.date_time_between(start_date=f"-{DAYS}d", end_date="now")
                extras.append({
                    "tenant_id": t["id"],
                    "amount": PRICE_MAP[et],
                    "billing_time": pd.to_datetime(ts)
                })
        extra_df = pd.DataFrame(extras) if extras else pd.DataFrame(columns=["tenant_id","amount","billing_time"])
        out = pd.concat([base[["tenant_id","amount","billing_time"]], extra_df], ignore_index=True)
    else:
        out = billed  # fallback

    return out[["tenant_id","amount","billing_time"]]

def main():
    os.makedirs("/opt/airflow/data", exist_ok=True)

    all_usage = []
    all_billing = []

    for t in TENANTS:
        u = gen_usage_for_tenant(t)
        b = gen_billing_for_tenant(u, t)
        all_usage.append(u)
        all_billing.append(b)

    usage_df = pd.concat(all_usage, ignore_index=True)
    billing_df = pd.concat(all_billing, ignore_index=True)

    usage_df.to_csv("/opt/airflow/data/usage_events.csv", index=False)
    billing_df.to_csv("/opt/airflow/data/billing_records.csv", index=False)

    print(f"Usage rows:   {len(usage_df):,}")
    print(f"Billing rows: {len(billing_df):,}")
    print("Tenants:", ", ".join([t["id"] for t in TENANTS]))

if __name__ == "__main__":
    main()
