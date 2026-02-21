"""
Generate realistic telecom customer data for segmentation analysis
This creates dummy data that mimics real telecom customer behavior
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Number of customers
n_customers = 3000

# Generate customer IDs
customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, n_customers + 1)]

# Generate account creation dates (past 5 years)
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)
account_ages_days = np.random.randint(30, 5*365, n_customers)
account_created = [end_date - timedelta(days=int(age)) for age in account_ages_days]

# Contract types with realistic distribution
contract_types = np.random.choice(
    ['Monthly', 'Quarterly', 'Annual'], 
    size=n_customers, 
    p=[0.55, 0.25, 0.20]  # 55% monthly, 25% quarterly, 20% annual
)

# Generate monthly charges based on contract type
monthly_charges = []
for contract in contract_types:
    if contract == 'Monthly':
        charge = np.random.normal(45, 15)  # Average $45, varies more
    elif contract == 'Quarterly':
        charge = np.random.normal(40, 10)  # Slight discount
    else:  # Annual
        charge = np.random.normal(35, 8)   # Best discount
    monthly_charges.append(max(15, charge))  # Minimum $15

monthly_charges = np.array(monthly_charges)

# Data usage (GB) - correlated with charges
data_usage = []
for charge in monthly_charges:
    if charge < 30:
        usage = np.random.normal(5, 2)
    elif charge < 50:
        usage = np.random.normal(15, 5)
    else:
        usage = np.random.normal(35, 10)
    data_usage.append(max(0.5, usage))

data_usage = np.array(data_usage)

# Call minutes - varies by customer type
call_minutes = []
for i in range(n_customers):
    if monthly_charges[i] < 30:
        minutes = np.random.normal(200, 100)
    elif monthly_charges[i] < 50:
        minutes = np.random.normal(500, 200)
    else:
        minutes = np.random.normal(1000, 300)
    call_minutes.append(max(0, minutes))

call_minutes = np.array(call_minutes)

# SMS usage
sms_sent = np.random.poisson(150, n_customers)

# Payment methods
payment_methods = np.random.choice(
    ['Credit Card', 'Bank Transfer', 'Digital Wallet', 'Cash'],
    size=n_customers,
    p=[0.45, 0.30, 0.20, 0.05]
)

# Late payments (more common with monthly contracts)
late_payments = []
for contract in contract_types:
    if contract == 'Monthly':
        late = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
    elif contract == 'Quarterly':
        late = np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05])
    else:  # Annual
        late = np.random.choice([0, 1], p=[0.9, 0.1])
    late_payments.append(late)

# Customer support calls
support_calls = np.random.poisson(2, n_customers)

# International calls (yes/no)
international_calls = np.random.choice(['Yes', 'No'], size=n_customers, p=[0.3, 0.7])

# Device type
device_types = np.random.choice(
    ['Smartphone', 'Feature Phone', 'Multiple Devices'],
    size=n_customers,
    p=[0.65, 0.15, 0.20]
)

# Churn status (whether customer left) - correlated with late payments and support calls
churn = []
for i in range(n_customers):
    churn_prob = 0.15  # Base 15% churn rate
    
    # Increase churn probability based on late payments
    churn_prob += late_payments[i] * 0.05
    
    # Increase churn probability based on support calls
    if support_calls[i] > 4:
        churn_prob += 0.15
    
    # Decrease churn probability for annual contracts
    if contract_types[i] == 'Annual':
        churn_prob -= 0.10
    
    # Decrease churn probability for longer tenure
    if account_ages_days[i] > 730:  # > 2 years
        churn_prob -= 0.08
        
    churn_prob = max(0, min(1, churn_prob))  # Keep between 0 and 1
    churn.append(np.random.choice(['Yes', 'No'], p=[churn_prob, 1-churn_prob]))

# Calculate total revenue (lifetime value)
total_revenue = monthly_charges * (account_ages_days / 30)

# Create DataFrame
df = pd.DataFrame({
    'customer_id': customer_ids,
    'account_created': account_created,
    'account_age_days': account_ages_days,
    'contract_type': contract_types,
    'monthly_charge': np.round(monthly_charges, 2),
    'data_usage_gb': np.round(data_usage, 2),
    'call_minutes': np.round(call_minutes, 0),
    'sms_sent': sms_sent,
    'payment_method': payment_methods,
    'late_payments': late_payments,
    'support_calls': support_calls,
    'international_calls': international_calls,
    'device_type': device_types,
    'total_revenue': np.round(total_revenue, 2),
    'churned': churn
})

# Save to CSV
df.to_csv('telecom_customers.csv', index=False)

print(f"✅ Generated data for {n_customers} customers")
print(f"📁 Saved to: telecom_customers.csv")
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nBasic statistics:")
print(df.describe())
print(f"\nChurn rate: {(df['churned'] == 'Yes').sum() / len(df) * 100:.1f}%")
