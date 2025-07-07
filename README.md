# RevMatch – Revenue Leak Detector for Usage-Based SaaS

 RevMatch is a production-grade data engineering pipeline that helps SaaS companies detect and fix hidden revenue leaks by matching real product usage data to billing records — before it hits the bottom line.


## What It Does

**RevMatch** simulates how a modern SaaS company might:
- Track customer usage (e.g., API calls, feature usage, credit spend)
- Bill customers monthly based on that usage
- Accidentally miss billables due to bugs, sync issues, or bad logic

RevMatch analyzes both data streams and finds **mismatches** between:
- What your customers used  
- What they were actually billed

> If your app logged 1,000 API calls but only billed 600... RevMatch finds that.


## Why It Matters

**SaaS companies lose millions** each year from:
- Underbilling
- Missing product event logs
- Feature misclassification
- Billing system integration failures

RevMatch helps **data teams, finance ops, and platform engineers** identify and eliminate these silent revenue killers — using real data engineering tools.


## Project Architecture

RevMatch is split into 4 modular layers:

### 1. **Data Simulation (Mock Ingestion)**
- Generates realistic **usage events** (e.g., API calls, report generations)
- Generates **billing records** based on partial/mismatched logic
- Teaches: how data enters modern SaaS systems

### 2. **Data Orchestration & ETL**
- Uses **Apache Airflow** to schedule, run, and track the pipeline
- Cleans, joins, and enriches usage + billing data

### 3. **Data Modeling with dbt**
- Transforms raw logs into:
  - `stg_usage_events`
  - `stg_billing_records`
  - `revmatch_leaks` — the money finder
- Models include tests, documentation, and descriptions

### 4. **Insights & Access**
- **FastAPI**: REST API for querying revenue mismatches
- **Looker Studio Dashboard**: Track leakage by customer, month, amount
- Optional: webhook/email alerts for large leaks


## Tech Stack (Real-World & Recruiter-Approved)

| Layer | Tech | Why |
|-------|------|-----|
| **Ingestion** | Python (Faker, mock generators) | Simulates SaaS product & billing logs |
| **Orchestration** | Apache Airflow | The industry standard for scheduling pipelines |
| **Transformations** | dbt | Clean, testable SQL transformations |
| **Warehouse** | BigQuery (or DuckDB for local dev) | Used by real data teams at scale |
| **API Layer** | FastAPI | Lightweight backend to expose leakage data |
| **Dashboard** | Looker Studio (or Streamlit) | Show business insights visually |
| **Infra** | Docker Compose | Run everything with one command — like a real data stack |


## Example Use Case

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
