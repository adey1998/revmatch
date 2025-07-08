import json
import random
from faker import Faker
from datetime import datetime

fake = Faker()

tenants = ["acme_saas", "globex", "initech"] # pretending to have 3 SaaS clients
events = ["api_call", "report_generation", "data_export"] # doing 3 types of product actions

# create 1 fake usage event (e.g., “acme_saas made an API call on June 10”)
def generate_usage_event(tenant):
    return {
        "tenantId": tenant,
        "event": random.choice(events),
        "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat()
    }

# intentionally bills for only 40%-90% of events (to simulate bugs/underbilling)
def generate_billing_record(tenant, total_events):
    billed_events = int(total_events * random.uniform(0.4, 0.9))
    return {
        "tenantId": tenant,
        "billedEvents": billed_events,
        "amountBilled": billed_events * 0.1,
        "timestamp": datetime.now().isoformat()
    }

def main():
    usage_logs = []
    billing_logs = []

    for tenant in tenants:
        event_count = random.randint(100, 200)
        usage_logs += [generate_usage_event(tenant) for _ in range(event_count)]
        billing_logs.append(generate_billing_record(tenant, event_count))

    with open("data/usage_events.json", "w") as f:
        json.dump(usage_logs, f, indent=2)
    
    with open("data/billing_records.json", "w") as f:
        json.dump(billing_logs, f, indent=2)

if __name__ == "__main__":
    main()