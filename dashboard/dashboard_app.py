import streamlit as st
from google.cloud import bigquery
import pandas as pd
import altair as alt
from datetime import date

# BigQuery Config
PROJECT_ID = "revmatch-project"
DATASET = "revmatch"
client = bigquery.Client(project=PROJECT_ID)

@st.cache_data(ttl=600)
def run_query(query: str) -> pd.DataFrame:
    return client.query(query).to_dataframe()

# Streamlit Layout
st.set_page_config(page_title="RevMatch Dashboard", layout="wide")
st.title("RevMatch Revenue Leak Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
tenant_filter = st.sidebar.text_input("Tenant ID")
date_range = st.sidebar.date_input("Date Range (for Daily Revenue)", [])

# Revenue Leak Section
st.markdown("## Revenue Leaks")

leaks_query = f"SELECT * FROM `{PROJECT_ID}.{DATASET}.revenue_leaks`"
if tenant_filter:
    leaks_query += f" WHERE tenant_id = '{tenant_filter}'"

leaks_df = run_query(leaks_query)

if not leaks_df.empty:
    # KPIs
    total_leak = leaks_df["leak_amount"].sum()
    underbilled = (leaks_df["status"] == "UNDERBILLED").sum()
    overbilled = (leaks_df["status"] == "OVERBILLED").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leak Amount", f"${total_leak:,.2f}")
    col2.metric("Underbilled Tenants", underbilled)
    col3.metric("Overbilled Tenants", overbilled)

    # Horizontal bar chart
    st.markdown("### Leak Breakdown by Tenant")
    bar = alt.Chart(leaks_df).mark_bar(size=40).encode(
        y=alt.Y("tenant_id:N", sort="-x", title="Tenant"),
        x=alt.X("leak_amount:Q", title="Leak Amount ($)"),
        color=alt.condition(
            alt.datum.leak_amount > 0,
            alt.value("orange"),  # Underbilled
            alt.value("red")      # Overbilled
        ),
        tooltip=["tenant_id", "expected_bill", "actual_bill", "leak_amount", "status"]
    ).properties(height=300)

    # Label outside the bar for readability
    labels = alt.Chart(leaks_df).mark_text(
        align="left",
        baseline="middle",
        dx=5,  # distance from bar
        fontSize=12,
        color="white" if leaks_df["leak_amount"].iloc[0] > 0 else "black"
    ).encode(
        y=alt.Y("tenant_id:N", sort="-x"),
        x=alt.X("leak_amount:Q"),
        text=alt.Text("leak_amount:Q", format=".2f")
    )

    st.altair_chart(bar + labels, use_container_width=True)

    # Raw table
    with st.expander("View Full Leak Table"):
        st.dataframe(leaks_df)

else:
    st.info("No revenue leaks found for the current filters.")

# Tenant Metrics Section
st.markdown("## Tenant Metrics")

metrics_query = f"SELECT * FROM `{PROJECT_ID}.{DATASET}.tenant_metrics`"
if tenant_filter:
    metrics_query += f" WHERE tenant_id = '{tenant_filter}'"

metrics_df = run_query(metrics_query)

if not metrics_df.empty:
    st.dataframe(metrics_df.sort_values(by="total_revenue", ascending=False))
else:
    st.info("No tenant metrics available for the current filters.")

# Daily Revenue Trend Section
if isinstance(date_range, list) and len(date_range) == 2:
    st.markdown("## Daily Revenue Trends")

    start_date, end_date = date_range
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    daily_query = f"""
        SELECT tenant_id, event_date, daily_revenue
        FROM `{PROJECT_ID}.{DATASET}.daily_revenue`
        WHERE event_date BETWEEN '{start_str}' AND '{end_str}'
    """
    if tenant_filter:
        daily_query += f" AND tenant_id = '{tenant_filter}'"

    daily_df = run_query(daily_query)

    if not daily_df.empty:
        # Format for line chart
        line_chart = alt.Chart(daily_df).mark_line(point=True).encode(
            x=alt.X("event_date:T", title="Date"),
            y=alt.Y("daily_revenue:Q", title="Revenue"),
            color="tenant_id:N",
            tooltip=["event_date:T", "tenant_id:N", "daily_revenue:Q"]
        ).properties(height=400)

        st.altair_chart(line_chart, use_container_width=True)

    else:
        st.info("No daily revenue data found for the selected date range.")
