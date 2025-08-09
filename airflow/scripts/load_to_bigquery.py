import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "revmatch-project"   # ← update if needed
DATASET    = "revmatch"

TABLE_USAGE   = f"{PROJECT_ID}.{DATASET}.usage_events"
TABLE_BILLING = f"{PROJECT_ID}.{DATASET}.billing_records"

def load_csv(path, table_id):
    df = pd.read_csv(path)

    # Make sure timestamps are parsed correctly
    for col in ["timestamp", "billing_time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], utc=True)

    client = bigquery.Client(project=PROJECT_ID)
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    )
    job.result()
    print(f"Loaded {len(df)} rows into {table_id}")

if __name__ == "__main__":
    client = bigquery.Client(project=PROJECT_ID)
    client.create_dataset(bigquery.Dataset(f"{PROJECT_ID}.{DATASET}"), exists_ok=True)

    load_csv("/opt/airflow/data/usage_events.csv",   TABLE_USAGE)
    load_csv("/opt/airflow/data/billing_records.csv", TABLE_BILLING)
