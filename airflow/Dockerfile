FROM apache/airflow:2.9.1-python3.10

USER root

# Install system packages
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
