# RevMatch – Revenue Leak Detector for Usage-Based SaaS

RevMatch is a production-grade data engineering pipeline that helps SaaS companies detect and fix hidden revenue leaks by matching real product usage data to billing records — before it hits the bottom line. 💸


## 🚀 What It Does

RevMatch simulates how a modern SaaS company might:

- Track customer usage (e.g., API calls, feature usage, credit spend)  
- Bill customers monthly based on that usage  
- Accidentally miss billables due to bugs, sync issues, or bad logic  

RevMatch analyzes both data streams and finds mismatches between:

- What your customers used  
- What they were actually billed  

> If your app logged 1,000 API calls but only billed 600... RevMatch finds that.


## ❓ Why It Matters

SaaS companies lose millions each year from:

- Underbilling  
- Missing product event logs  
- Feature misclassification  
- Billing system integration failures  

RevMatch helps data teams, finance ops, and platform engineers identify and eliminate these silent revenue killers — using real data engineering tools. 


## 🧠 Architecture Overview

RevMatch is split into 4 modular layers:

### 1. Data Simulation (Mock Ingestion)  
- Generates realistic usage events (e.g., API calls, report generations)  
- Generates billing records based on partial/mismatched logic  
- *Teaches:* how data enters modern SaaS systems  

### 2. Data Orchestration & ETL  
- Uses Apache Airflow to schedule, run, and track the pipeline  
- Cleans, joins, and enriches usage + billing data  

### 3. Data Modeling with dbt  
- Transforms raw logs into:  
  - `stg_usage_events`  
  - `stg_billing_records`  
  - `revmatch_leaks` — the money finder  
- Includes model testing, documentation, and lineage  

### 4. Insights & Access  
- FastAPI: REST API for querying revenue mismatches  
- Looker Studio Dashboard: Visualize leakage by customer, month, amount  
- Optional: webhook/email alerts for large leaks


## 🧱 Tech Stack

| Layer         | Tech                            | Why                                     |
|---------------|----------------------------------|------------------------------------------|
| Ingestion     | Python (Faker, mock generators)  | Simulates SaaS product & billing logs   |
| Orchestration | Apache Airflow                  | The industry standard for pipelines     |
| Transform     | dbt                              | Clean, testable SQL transformations     |
| Warehouse     | BigQuery                         | Used by real data teams at scale        |
| API Layer     | FastAPI                          | Lightweight backend for leak data       |
| Dashboard     | Looker Studio / Streamlit        | Visual insights for business users      |
| Infra         | Docker Compose                  | Run everything with one command         |


## 🧩 Architectural Pattern

RevMatch follows a modular, real-world data stack pattern often seen in modern SaaS companies:

- **Event-Driven Ingestion** — Mock usage + billing logs simulate real product behavior  
- **Batch-Oriented ETL** — Apache Airflow runs scheduled batch jobs  
- **ELT with dbt** — Raw → Staging → Business models in SQL  
- **API Layer & Dashboard** — Expose results via REST and visual dashboards  
- **Composable Infra** — Each service runs independently via Docker Compose  


## 🧪 Testing

- `pytest` for API layer (FastAPI endpoints)  
- `dbt test` for model assumptions: nulls, uniqueness, relationships  
- Manual DAG testing via Airflow UI or CLI  
- Optional unit tests for ingestion logic and data validation  

Example CLI test:  
```bash
http GET localhost:8000/leaks/tenant/acme_saas
```
## 👷 Built For

RevMatch is designed to support:

- **Data Engineers** – Build production-grade pipelines  
- **Analytics Engineers** – Own dbt models and insights  
- **Finance Ops** – Identify billing anomalies early  
- **Platform Engineers** – Validate event logging integrity  
- **SaaS Startups & Scaleups** – Avoid silent revenue loss as you grow  

## 📦 Example Use Case

```json
{
  "tenantId": "acme_saas",
  "expectedBill": 240.00,
  "actualBill": 120.00,
  "leakAmount": 120.00,
  "unbilledEvents": [
    { "event": "api_call", "timestamp": "2025-07-06T03:23:00Z" },
    { "event": "report_generation", "timestamp": "2025-07-06T04:02:00Z" }
  ],
  "status": "underbilled",
  "lastChecked": "2025-07-07T15:41:00Z"
}
```

## 📷 Screenshots

Full walkthrough, screenshots, and feature breakdown available at:

🔗 [RevMatch Project Page](https://arvildey.com/projects/revmatch)

## 📜 License

This project is licensed under the [MIT License](LICENSE). 


