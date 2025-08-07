import pandas as pd
from google.cloud import bigquery
import os

# Your GCP settings
PROJECT_ID = "revmatch-project"    # ← replace with your actual Project ID
DATASET    = "revmatch"            # ← load into the "revmatch" dataset

# Fully qualified table IDs
TABLE_USAGE   = f"{PROJECT_ID}.{DATASET}.usage_events"
TABLE_BILLING = f"{PROJECT_ID}.{DATASET}.billing_records"

def load_csv(path, table_id, client):
    df = pd.read_csv(path)
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # wait for job to finish
    print(f"Loaded {len(df)} rows into {table_id}")

if __name__ == "__main__":
    # Ensure credentials env var is set by your Docker Compose:
    # GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/keys/gcp-key.json

    # Initialize BigQuery client
    client = bigquery.Client(project=PROJECT_ID)

    # Auto-create the dataset if missing
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET}")
    client.create_dataset(dataset_ref, exists_ok=True)

    # Load both CSVs
    load_csv("/opt/airflow/data/usage_events.csv",   TABLE_USAGE,   client)
    load_csv("/opt/airflow/data/billing_records.csv", TABLE_BILLING, client)
