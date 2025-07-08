from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import json

# Load step in ELT
def extract_transform():
    with open("data/usage_events.json") as f:
        usage = json.load(f)
    with open("data/billing_records.json") as f:
        billing = json.load(f)

    # save to CSVs so dbt can use them
    pd.DataFrame(usage).to_csv("dbt/models/staging/usage_events.csv", index=False)
    pd.DataFrame(billing).to_csv("dbt/models/staging/billing_records.csv", index=False)

default_args = {
    "start_date": datetime(2025, 1, 1)
}

with DAG("revmatch_pipeline", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:
    etl_task = PythonOperator(
        task_id="extract_transform",
        python_callable=extract_transform
    )

if __name__ == "__main__":
    extract_transform()