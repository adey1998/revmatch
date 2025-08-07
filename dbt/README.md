# RevMatch dbt Project

This dbt project powers the **transformation layer** of RevMatch – a data engineering pipeline that detects revenue leaks in usage-based SaaS billing.

## How It Works

RevMatch uses **dbt** to transform raw SaaS usage and billing data into clean, analytics-ready models. Here's the flow:

### **Data Flow**
1. **Raw Data → Seeds**
   - `usage_events.csv` and `billing_records.csv` are seeded into BigQuery using:
     ```bash
     dbt seed
     ```

2. **Staging Models**
   - Standardize and clean raw data for consistency.
   - Models:
     - `stg_usage_events`
     - `stg_billing_records`

3. **Intermediate Models**
   - Aggregate and derive metrics for analysis.
   - Example:
     - `daily_revenue.sql` → Summarizes usage & billing by date and tenant.

4. **Core Models**
   - Apply business logic to detect revenue leakage and compute tenant metrics.
   - Models:
     - `metrics/revenue_leaks.sql` → Identifies underbilling gaps.
     - `metrics/tenant_metrics.sql` → Aggregates performance per tenant.

### **Execution Order**
- dbt automatically runs models based on dependencies:
  raw → staging → intermediate → core

## Data Lineage
Here’s the dependency flow:

![Lineage Graph](./docs/images/lineage_graph.png)

## **Key Commands**
Run all models:
```dbt run```

Load seed data:
```dbt seed```

Test data integrity:
```dbt test```