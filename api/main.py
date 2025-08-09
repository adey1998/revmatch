from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from typing import List

PROJECT_ID = "revmatch-project"
DATASET    = "revmatch"

app = FastAPI(title="RevMatch API")
client = bigquery.Client(project=PROJECT_ID)

# Pydantic schemas
class Leak(BaseModel):
    tenant_id: str
    expected_bill: float
    actual_bill: float
    leak_amount: float
    status: str

class TenantMetric(BaseModel):
    tenant_id: str
    active_days: int
    total_revenue: float
    avg_daily_revenue: float


def query_table(table_name: str):
    sql = f"""
            SELECT *
            FROM `{PROJECT_ID}.{DATASET}.{table_name}`
            LIMIT 1000
        """
    try:
        rows = client.query(sql).result()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endopoints    
@app.get("/leaks", response_model=List[Leak])
def get_leaks():
    return query_table("revenue_leaks")

@app.get("/metrics", response_model=List[TenantMetric])
def get_metrics():
    return query_table("tenant_metrics")