"""
Synthetic Banking Data Generator
Generates realistic, internally consistent banking datasets for analytics.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os

# Initialize
fake = Faker()
np.random.seed(42)
Faker.seed(42)

# Configuration
NUM_CUSTOMERS = 10000
NUM_ACCOUNTS = 15000
NUM_LOANS = 5000
NUM_TRANSACTIONS = 100000
NUM_COSTS = 1000
MONTHS_MACRO = 24

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_customers():
    """Generate customer master data."""
    print("Generating customers...")
    
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            'customer_id': i,
            'customer_name': fake.name(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
            'customer_segment': np.random.choice(['Retail', 'SME', 'Corporate'], p=[0.7, 0.2, 0.1]),
            'credit_score': int(np.random.normal(680, 80)),
            'registration_date': fake.date_between(start_date='-5y', end_date='today'),
            'city': fake.city(),
            'country': 'USA'
        })
    
    df = pd.DataFrame(customers)
    df['credit_score'] = df['credit_score'].clip(300, 850)
    df.to_csv(f'{OUTPUT_DIR}/customers.csv', index=False)
    print(f"✓ Created customers.csv with {len(df)} records")
    return df


def generate_accounts(customers_df):
    """Generate account data linked to customers."""
    print("Generating accounts...")
    
    accounts = []
    account_id = 1
    
    for customer_id in customers_df['customer_id']:
        num_accounts = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
        
        for _ in range(num_accounts):
            if account_id > NUM_ACCOUNTS:
                break
                
            accounts.append({
                'account_id': account_id,
                'customer_id': customer_id,
                'account_type': np.random.choice(['Checking', 'Savings', 'Investment'], p=[0.5, 0.3, 0.2]),
                'account_status': np.random.choice(['Active', 'Dormant', 'Closed'], p=[0.85, 0.10, 0.05]),
                'opening_date': fake.date_between(start_date='-4y', end_date='today'),
                'current_balance': round(np.random.lognormal(8, 2), 2),
                'currency': 'USD'
            })
            account_id += 1
            
        if account_id > NUM_ACCOUNTS:
            break
    
    df = pd.DataFrame(accounts)
    df['current_balance'] = df['current_balance'].clip(0, 1000000)
    df.to_csv(f'{OUTPUT_DIR}/accounts.csv', index=False)
    print(f"✓ Created accounts.csv with {len(df)} records")
    return df


def generate_loans(customers_df):
    """Generate loan data with credit risk parameters."""
    print("Generating loans...")
    
    # Sample customers for loans
    loan_customers = customers_df.sample(n=NUM_LOANS, replace=True)
    
    loans = []
    for idx, row in loan_customers.iterrows():
        credit_score = row['credit_score']
        
        # PD based on credit score
        if credit_score >= 750:
            pd = np.random.uniform(0.005, 0.02)
        elif credit_score >= 650:
            pd = np.random.uniform(0.02, 0.05)
        elif credit_score >= 550:
            pd = np.random.uniform(0.05, 0.12)
        else:
            pd = np.random.uniform(0.12, 0.25)
        
        # LGD (Loss Given Default)
        lgd = np.random.uniform(0.30, 0.65)
        
        # Loan details
        loan_amount = round(np.random.lognormal(10, 1.5), 2)
        outstanding_balance = loan_amount * np.random.uniform(0.3, 1.0)
        
        # Delinquency status
        status_probs = [0.85, 0.08, 0.04, 0.03] if pd < 0.05 else [0.70, 0.15, 0.10, 0.05]
        loan_status = np.random.choice(['Current', 'DPD_30', 'DPD_90', 'Default'], p=status_probs)
        
        # EAD = outstanding balance
        ead = outstanding_balance
        
        # ECL = PD * LGD * EAD
        ecl = pd * lgd * ead
        
        loans.append({
            'loan_id': len(loans) + 1,
            'customer_id': row['customer_id'],
            'loan_type': np.random.choice(['Personal', 'Mortgage', 'Auto', 'Business'], p=[0.3, 0.35, 0.25, 0.1]),
            'origination_date': fake.date_between(start_date='-3y', end_date='-6m'),
            'maturity_date': fake.date_between(start_date='today', end_date='+10y'),
            'original_amount': round(loan_amount, 2),
            'outstanding_balance': round(outstanding_balance, 2),
            'interest_rate': round(np.random.uniform(3.5, 12.5), 2),
            'loan_status': loan_status,
            'days_past_due': 0 if loan_status == 'Current' else (30 if loan_status == 'DPD_30' else (90 if loan_status == 'DPD_90' else 120)),
            'pd': round(pd, 4),
            'lgd': round(lgd, 4),
            'ead': round(ead, 2),
            'ecl': round(ecl, 2)
        })
    
    df = pd.DataFrame(loans)
    df.to_csv(f'{OUTPUT_DIR}/loans.csv', index=False)
    print(f"✓ Created loans.csv with {len(df)} records")
    return df


def generate_transactions(accounts_df):
    """Generate transaction data."""
    print("Generating transactions...")
    
    # Sample accounts for transactions
    active_accounts = accounts_df[accounts_df['account_status'] == 'Active']
    
    transactions = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(NUM_TRANSACTIONS):
        account = active_accounts.sample(n=1).iloc[0]
        
        trans_date = start_date + timedelta(days=np.random.randint(0, 365))
        
        trans_type = np.random.choice(['Debit', 'Credit', 'Fee', 'Interest'], p=[0.45, 0.40, 0.10, 0.05])
        
        if trans_type == 'Debit':
            amount = round(np.random.lognormal(3, 1.5), 2)
            category = np.random.choice(['Shopping', 'Dining', 'Bills', 'Transfer', 'ATM'])
        elif trans_type == 'Credit':
            amount = round(np.random.lognormal(4, 1.5), 2)
            category = np.random.choice(['Salary', 'Transfer', 'Refund', 'Investment'])
        elif trans_type == 'Fee':
            amount = round(np.random.uniform(5, 50), 2)
            category = 'Service_Fee'
        else:
            amount = round(account['current_balance'] * np.random.uniform(0.0001, 0.002), 2)
            category = 'Interest_Income'
        
        transactions.append({
            'transaction_id': i + 1,
            'account_id': account['account_id'],
            'customer_id': account['customer_id'],
            'transaction_date': trans_date.strftime('%Y-%m-%d'),
            'transaction_type': trans_type,
            'amount': amount,
            'category': category,
            'description': f"{trans_type} - {category}"
        })
    
    df = pd.DataFrame(transactions)
    df.to_csv(f'{OUTPUT_DIR}/transactions.csv', index=False)
    print(f"✓ Created transactions.csv with {len(df)} records")
    return df


def generate_costs():
    """Generate cost data with budget variance and leakage."""
    print("Generating costs...")
    
    costs = []
    start_date = datetime.now() - timedelta(days=730)
    
    business_units = ['Retail Banking', 'Corporate Banking', 'Operations', 'Technology', 'Risk Management']
    cost_categories = ['Personnel', 'Technology', 'Marketing', 'Facilities', 'Compliance', 'Other']
    vendors = [fake.company() for _ in range(20)]
    
    for i in range(NUM_COSTS):
        month = start_date + timedelta(days=30 * i)
        
        bu = np.random.choice(business_units)
        category = np.random.choice(cost_categories)
        vendor = np.random.choice(vendors)
        
        # Budget
        budget = round(np.random.lognormal(10, 1.5), 2)
        
        # Actual with variance and occasional leakage
        if np.random.random() < 0.15:
            variance_pct = np.random.uniform(0.20, 0.50)
        else:
            variance_pct = np.random.normal(0, 0.10)
        
        actual = budget * (1 + variance_pct)
        
        costs.append({
            'cost_id': i + 1,
            'cost_date': month.strftime('%Y-%m-%d'),
            'business_unit': bu,
            'cost_category': category,
            'vendor': vendor,
            'budget_amount': round(budget, 2),
            'actual_amount': round(actual, 2),
            'variance_amount': round(actual - budget, 2),
            'variance_pct': round(variance_pct, 4)
        })
    
    df = pd.DataFrame(costs)
    df.to_csv(f'{OUTPUT_DIR}/costs.csv', index=False)
    print(f"✓ Created costs.csv with {len(df)} records")
    return df


def generate_macro():
    """Generate macroeconomic indicators."""
    print("Generating macro indicators...")
    
    macro = []
    start_date = datetime.now() - timedelta(days=730)
    
    for i in range(MONTHS_MACRO):
        month = start_date + timedelta(days=30 * i)
        
        # Base values with trends
        gdp_growth = 2.5 + np.random.normal(0, 0.5) + (i * 0.01)
        unemployment = 5.0 + np.random.normal(0, 0.3) - (i * 0.01)
        interest_rate = 3.0 + np.random.normal(0, 0.2) + (i * 0.02)
        inflation = 2.0 + np.random.normal(0, 0.3) + (i * 0.015)
        
        macro.append({
            'date': month.strftime('%Y-%m-%d'),
            'gdp_growth_rate': round(gdp_growth, 2),
            'unemployment_rate': round(max(unemployment, 3.0), 2),
            'interest_rate': round(max(interest_rate, 0.5), 2),
            'inflation_rate': round(inflation, 2),
            'consumer_confidence_index': round(np.random.uniform(80, 120), 1)
        })
    
    df = pd.DataFrame(macro)
    df.to_csv(f'{OUTPUT_DIR}/macro.csv', index=False)
    print(f"✓ Created macro.csv with {len(df)} records")
    return df


def main():
    """Main execution."""
    print("\n" + "="*60)
    print("FINANCIAL DATA GENERATOR")
    print("="*60 + "\n")
    
    # Generate all datasets
    customers_df = generate_customers()
    accounts_df = generate_accounts(customers_df)
    loans_df = generate_loans(customers_df)
    transactions_df = generate_transactions(accounts_df)
    costs_df = generate_costs()
    macro_df = generate_macro()
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"\nAll files saved to: {OUTPUT_DIR}/")
    print("\nDataset Summary:")
    print(f"  • Customers:     {len(customers_df):,}")
    print(f"  • Accounts:      {len(accounts_df):,}")
    print(f"  • Loans:         {len(loans_df):,}")
    print(f"  • Transactions:  {len(transactions_df):,}")
    print(f"  • Costs:         {len(costs_df):,}")
    print(f"  • Macro records: {len(macro_df):,}")
    print("\n✓ Ready for database load!")


if __name__ == "__main__":
    main()
