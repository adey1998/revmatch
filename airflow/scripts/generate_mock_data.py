import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
NUM_EVENTS = 1000
TENANT_ID = "acme_saas"

def generate_usage_events():
    events = []
    for _ in range(NUM_EVENTS):
        event_type = random.choice(["api_call", "report_generation", "dashboard_view"])
        timestamp = fake.date_time_between(start_date="-30d", end_date="now")
        events.append({
            "tenant_id": TENANT_ID,
            "event": event_type,
            "timestamp": timestamp.isoformat()
        })
    return pd.DataFrame(events)

def generate_billing_records(usage_df):
    # Bill 60% of events to simulate underbilling
    billed_df = usage_df.sample(frac=0.6, random_state=42).copy()
    billed_df["amount"] = billed_df["event"].map({
        "api_call": 0.10,
        "report_generation": 0.50,
        "dashboard_view": 0.05
    })
    summary = billed_df.groupby("tenant_id")["amount"].sum().reset_index()
    summary["billed_at"] = datetime.utcnow().isoformat()
    return summary

if __name__ == "__main__":
    os.makedirs("/opt/airflow/data", exist_ok=True)
    usage_df = generate_usage_events()
    billing_df = generate_billing_records(usage_df)

    usage_path = "/opt/airflow/data/usage_events.csv"
    billing_path = "/opt/airflow/data/billing_records.csv"

    usage_df.to_csv(usage_path, index=False)
    billing_df.to_csv(billing_path, index=False)

    print(f"Generated {len(usage_df)} usage events → {usage_path}")
    print(f"Generated {len(billing_df)} billing rows → {billing_path}")
