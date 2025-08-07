from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {
    "start_date": datetime(2025, 1, 1),
    "catchup": False
}

def run_script(script_path):
    subprocess.run(["python", script_path], check=True)

with DAG(
    dag_id="revmatch_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    tags=["revmatch"]
) as dag:

    generate_data = PythonOperator(
        task_id="generate_mock_data",
        python_callable=run_script,
        op_args=["/opt/airflow/scripts/generate_mock_data.py"]
    )

    load_bq = PythonOperator(
        task_id="load_to_bigquery",
        python_callable=run_script,
        op_args=["/opt/airflow/scripts/load_to_bigquery.py"]
    )

    generate_data >> load_bq