import pandas as pd
import numpy as np
import random

# Set a seed so the "random" data is reproducible — 
# anyone running this script gets the exact same dataset
np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 300

ARCHETYPES = {
    "healthy": 0.50,
    "at_risk": 0.30,
    "severely_at_risk": 0.15,
    "churned": 0.05,
}

# Randomly assign each of the 300 customers to an archetype,
# respecting the percentages we set above
archetype_assignments = np.random.choice(
    list(ARCHETYPES.keys()),
    size=NUM_CUSTOMERS,
    p=list(ARCHETYPES.values())
)

# Start building our dataset as a list of dictionaries — 
# one dictionary per customer, each tagged with their archetype
customers = []
for i in range(NUM_CUSTOMERS):
    customer = {
        "customer_id": f"CUST{i+1:04d}",  # e.g. CUST0001, CUST0002...
        "archetype": archetype_assignments[i],
    }
    customers.append(customer)

# Convert the list of dictionaries into a proper table (DataFrame)
df = pd.DataFrame(customers)

# Quick sanity check: print how many customers landed in each archetype
print(df["archetype"].value_counts())

def generate_usage_data(archetype):
    """Generate login counts for the 3 trend periods, based on archetype."""
    if archetype == "healthy":
        logins_recent = np.random.randint(20, 41)
        logins_mid = np.random.randint(18, 38)
        logins_old = np.random.randint(15, 35)
    elif archetype == "at_risk":
        logins_recent = np.random.randint(5, 18)
        logins_mid = np.random.randint(10, 22)
        logins_old = np.random.randint(15, 28)
    elif archetype == "severely_at_risk":
        logins_recent = np.random.randint(0, 6)
        logins_mid = np.random.randint(2, 10)
        logins_old = np.random.randint(5, 15)
    else:  # churned
        logins_recent = np.random.randint(0, 2)
        logins_mid = np.random.randint(0, 4)
        logins_old = np.random.randint(2, 10)

    return logins_recent, logins_mid, logins_old


# Apply this function to every customer and add the results as new columns
logins_last_30, logins_31_60, logins_61_90 = [], [], []

for archetype in df["archetype"]:
    recent, mid, old = generate_usage_data(archetype)
    logins_last_30.append(recent)
    logins_31_60.append(mid)
    logins_61_90.append(old)

df["logins_last_30_days"] = logins_last_30
df["logins_31_to_60_days_ago"] = logins_31_60
df["logins_61_to_90_days_ago"] = logins_61_90

print(df.head())

def generate_support_data(archetype):
    """Generate support ticket metrics based on archetype."""
    if archetype == "healthy":
        total_tickets = np.random.randint(0, 5)
        high_severity = np.random.randint(0, 1)
        open_tickets = np.random.randint(0, 2)
        avg_days_open = np.random.randint(0, 5) if open_tickets > 0 else 0
        resolved = total_tickets - open_tickets
        avg_resolution_days = np.random.randint(1, 4) if resolved > 0 else 0
    elif archetype == "at_risk":
        total_tickets = np.random.randint(3, 10)
        high_severity = np.random.randint(0, 3)
        open_tickets = np.random.randint(1, 4)
        avg_days_open = np.random.randint(3, 12) if open_tickets > 0 else 0
        resolved = total_tickets - open_tickets
        avg_resolution_days = np.random.randint(3, 8) if resolved > 0 else 0
    elif archetype == "severely_at_risk":
        total_tickets = np.random.randint(8, 20)
        high_severity = np.random.randint(2, 7)
        open_tickets = np.random.randint(3, 9)
        avg_days_open = np.random.randint(10, 30) if open_tickets > 0 else 0
        resolved = total_tickets - open_tickets
        avg_resolution_days = np.random.randint(7, 15) if resolved > 0 else 0
    else:  # churned
        total_tickets = np.random.randint(5, 18)
        high_severity = np.random.randint(3, 9)
        open_tickets = np.random.randint(2, 8)
        avg_days_open = np.random.randint(20, 60) if open_tickets > 0 else 0
        resolved = max(total_tickets - open_tickets, 0)
        avg_resolution_days = np.random.randint(10, 25) if resolved > 0 else 0

    return total_tickets, high_severity, open_tickets, avg_days_open, resolved, avg_resolution_days


# Apply to every customer
support_cols = {
    "support_tickets_last_90_days": [],
    "high_severity_tickets_last_90_days": [],
    "open_tickets_count": [],
    "avg_days_open_for_unresolved": [],
    "resolved_tickets_count": [],
    "avg_resolution_time_days": [],
}

for archetype in df["archetype"]:
    total, severe, open_t, days_open, resolved, res_days = generate_support_data(archetype)
    support_cols["support_tickets_last_90_days"].append(total)
    support_cols["high_severity_tickets_last_90_days"].append(severe)
    support_cols["open_tickets_count"].append(open_t)
    support_cols["avg_days_open_for_unresolved"].append(days_open)
    support_cols["resolved_tickets_count"].append(resolved)
    support_cols["avg_resolution_time_days"].append(res_days)

for col_name, values in support_cols.items():
    df[col_name] = values

print(df[["customer_id", "archetype"] + list(support_cols.keys())].head())

def generate_renewal_data(archetype):
    """Generate renewal, contact, and retention cadence metrics based on archetype."""
    contract_length = np.random.choice([12, 24, 36])

    if archetype == "healthy":
        days_until_renewal = np.random.randint(60, 365)
        touchpoints = np.random.randint(3, 8)
        days_since_contact = np.random.randint(0, 30)
        first_call_done = True
        one_month_done = True
        quarters_scheduled = np.random.randint(1, 5)
        quarters_completed = quarters_scheduled
    elif archetype == "at_risk":
        days_until_renewal = np.random.randint(20, 200)
        touchpoints = np.random.randint(1, 4)
        days_since_contact = np.random.randint(20, 70)
        first_call_done = True
        one_month_done = np.random.choice([True, False])
        quarters_scheduled = np.random.randint(1, 5)
        quarters_completed = max(quarters_scheduled - np.random.randint(0, 2), 0)
    elif archetype == "severely_at_risk":
        days_until_renewal = np.random.randint(1, 90)
        touchpoints = np.random.randint(0, 2)
        days_since_contact = np.random.randint(60, 150)
        first_call_done = np.random.choice([True, False])
        one_month_done = False
        quarters_scheduled = np.random.randint(2, 6)
        quarters_completed = max(quarters_scheduled - np.random.randint(2, 4), 0)
    else:  # churned
        days_until_renewal = np.random.randint(-60, 10)  # negative = already past renewal
        touchpoints = np.random.randint(0, 2)
        days_since_contact = np.random.randint(90, 200)
        first_call_done = np.random.choice([True, False])
        one_month_done = False
        quarters_scheduled = np.random.randint(2, 6)
        quarters_completed = max(quarters_scheduled - np.random.randint(3, 5), 0)

    return (contract_length, days_until_renewal, touchpoints, days_since_contact,
            first_call_done, one_month_done, quarters_scheduled, quarters_completed)


renewal_cols = {
    "contract_length_months": [],
    "days_until_renewal": [],
    "cs_touchpoints_last_90_days": [],
    "days_since_last_contact": [],
    "first_retention_call_completed": [],
    "one_month_checkin_completed": [],
    "quarterly_checkins_scheduled": [],
    "quarterly_checkins_completed": [],
}

for archetype in df["archetype"]:
    results = generate_renewal_data(archetype)
    for col_name, value in zip(renewal_cols.keys(), results):
        renewal_cols[col_name].append(value)

for col_name, values in renewal_cols.items():
    df[col_name] = values

print(df[["customer_id", "archetype"] + list(renewal_cols.keys())].head())

def generate_satisfaction_data(archetype):
    """Generate NPS, CSAT, and survey recency based on archetype."""
    if archetype == "healthy":
        nps = np.random.randint(30, 101)
        csat = np.random.randint(4, 6)
        days_since_survey = np.random.randint(0, 60)
    elif archetype == "at_risk":
        nps = np.random.randint(-10, 40)
        csat = np.random.randint(3, 5)
        days_since_survey = np.random.randint(30, 120)
    elif archetype == "severely_at_risk":
        nps = np.random.randint(-50, 10)
        csat = np.random.randint(1, 4)
        days_since_survey = np.random.randint(60, 200)
    else:  # churned
        nps = np.random.randint(-100, -10)
        csat = np.random.randint(1, 3)
        days_since_survey = np.random.randint(100, 300)

    return nps, csat, days_since_survey


satisfaction_cols = {
    "latest_nps_score": [],
    "latest_csat_score": [],
    "days_since_last_survey_response": [],
}

for archetype in df["archetype"]:
    nps, csat, days = generate_satisfaction_data(archetype)
    satisfaction_cols["latest_nps_score"].append(nps)
    satisfaction_cols["latest_csat_score"].append(csat)
    satisfaction_cols["days_since_last_survey_response"].append(days)

for col_name, values in satisfaction_cols.items():
    df[col_name] = values

print(df[["customer_id", "archetype"] + list(satisfaction_cols.keys())].head())