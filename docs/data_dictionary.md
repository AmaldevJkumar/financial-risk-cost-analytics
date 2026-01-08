# Data Dictionary

Complete field-level documentation for all tables in the Financial Risk & Cost Intelligence Platform.

---

## Raw Data Tables

### raw.customers

Customer master data containing demographic and credit information.

| Field Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| customer_id | INTEGER | Unique customer identifier | 12345 | PRIMARY KEY |
| customer_name | VARCHAR(200) | Full name of customer | John Smith | NOT NULL |
| date_of_birth | DATE | Customer's date of birth | 1985-03-15 | NOT NULL |
| customer_segment | VARCHAR(50) | Business segment classification | Retail | NOT NULL, IN ('Retail', 'SME', 'Corporate') |
| credit_score | INTEGER | FICO credit score | 720 | 300-850 |
| registration_date | DATE | Date customer joined bank | 2020-01-15 | NOT NULL |
| city | VARCHAR(100) | City of residence | New York | |
| country | VARCHAR(50) | Country of residence | USA | |

---

### raw.accounts

Account master data linked to customers.

| Field Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| account_id | INTEGER | Unique account identifier | 98765 | PRIMARY KEY |
| customer_id | INTEGER | Reference to customer | 12345 | FOREIGN KEY → customers |
| account_type | VARCHAR(50) | Type of account | Checking | IN ('Checking', 'Savings', 'Investment') |
| account_status | VARCHAR(20) | Current account status | Active | IN ('Active', 'Dormant', 'Closed') |
| opening_date | DATE | Date account was opened | 2020-02-01 | NOT NULL |
| current_balance | NUMERIC(15,2) | Current account balance | 5432.50 | >= 0 |
| currency | VARCHAR(3) | Currency code | USD | Default: USD |

---

### raw.loans

Loan portfolio with credit risk parameters.

| Field Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| loan_id | INTEGER | Unique loan identifier | 55555 | PRIMARY KEY |
| customer_id | INTEGER | Reference to customer | 12345 | FOREIGN KEY → customers |
| loan_type | VARCHAR(50) | Type of loan | Mortgage | IN ('Personal', 'Mortgage', 'Auto', 'Business') |
| origination_date | DATE | Loan origination date | 2021-06-15 | NOT NULL |
| maturity_date | DATE | Loan maturity date | 2031-06-15 | NOT NULL |
| original_amount | NUMERIC(15,2) | Original loan amount | 250000.00 | NOT NULL |
| outstanding_balance | NUMERIC(15,2) | Current outstanding balance | 235000.00 | NOT NULL |
| interest_rate | NUMERIC(5,2) | Annual interest rate (%) | 4.25 | NOT NULL |
| loan_status | VARCHAR(20) | Current loan status | Current | IN ('Current', 'DPD_30', 'DPD_90', 'Default') |
| days_past_due | INTEGER | Days payment is overdue | 0 | >= 0 |
| pd | NUMERIC(8,4) | Probability of Default | 0.0250 | 0.0-1.0 |
| lgd | NUMERIC(8,4) | Loss Given Default | 0.4000 | 0.0-1.0 |
| ead | NUMERIC(15,2) | Exposure at Default | 235000.00 | NOT NULL |
| ecl | NUMERIC(15,2) | Expected Credit Loss | 2350.00 | NOT NULL |

**Calculated Fields**:
- `ecl = pd × lgd × ead`

---

### raw.transactions

Transaction history for all accounts.

| Field Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| transaction_id | INTEGER | Unique transaction identifier | 777777 | PRIMARY KEY |
| account_id | INTEGER | Reference to account | 98765 | FOREIGN KEY → accounts |
| customer_id | INTEGER | Reference to customer | 12345 | FOREIGN KEY → customers |
| transaction_date | DATE | Date of transaction | 2024-01-15 | NOT NULL |
| transaction_type | VARCHAR(20) | Type of transaction | Credit | IN ('Debit', 'Credit', 'Fee', 'Interest') |
| amount | NUMERIC(15,2) | Transaction amount | 1500.00 | NOT NULL |
| category | VARCHAR(50) | Transaction category | Salary | |
| description | TEXT | Transaction description | Monthly salary deposit | |

**Transaction Types**:
- **Debit**: Money out (purchases, withdrawals)
- **Credit**: Money in (deposits, salary)
- **Fee**: Service charges
- **Interest**: Interest earned/charged

---

### raw.costs

Cost tracking with budget variance.

| Field Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| cost_id | INTEGER | Unique cost entry identifier | 11111 | PRIMARY KEY |
| cost_date | DATE | Date of cost entry | 2024-01-31 | NOT NULL |
| business_unit | VARCHAR(100) | Business unit incurring cost | Technology | NOT NULL |
| cost_category | VARCHAR(50) | Category of cost | Personnel | NOT NULL |
| vendor | VARCHAR(200) | Vendor/supplier name | Acme Corp | |
| budget_amount | NUMERIC(15,2) | Budgeted amount | 50000.00 | NOT NULL |
| actual_amount | NUMERIC(15,2) | Actual amount spent | 62000.00 | NOT NULL |
| variance_amount | NUMERIC(15,2) | Variance (Actual - Budget) | 12000.00 | NOT NULL |
| variance_pct | NUMERIC(8,4) | Variance percentage | 0.2400 | NOT NULL |

**Calculated Fields**:
- `variance_amount = actual_amount - budget_amount`
- `variance_pct = variance_amount / budget_amount`

**Business Units**:
- Retail Banking
- Corporate Banking
- Operations
- Technology
- Risk Management

**Cost Categories**:
- Personnel
- Technology
- Marketing
- Facilities
- Compliance
- Other

---

### raw.macro

Macroeconomic indicators for scenario analysis.

| Field Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| date | DATE | Date of observation | 2024-01-31 | PRIMARY KEY |
| gdp_growth_rate | NUMERIC(5,2) | GDP growth rate (%) | 2.50 | |
| unemployment_rate | NUMERIC(5,2) | Unemployment rate (%) | 4.10 | |
| interest_rate | NUMERIC(5,2) | Base interest rate (%) | 5.25 | |
| inflation_rate | NUMERIC(5,2) | Inflation rate (%) | 3.20 | |
| consumer_confidence_index | NUMERIC(5,1) | Consumer confidence index | 98.5 | |

---

## Analytics Output Tables

### monthly_kpis.csv

Monthly key performance indicators combining revenue, costs, and profitability.

| Field Name | Description | Example |
|------------|-------------|---------|
| month | Month in YYYY-MM format | 2024-01 |
| total_revenue | Total revenue for month | 1250000.00 |
| fee_revenue | Revenue from fees | 450000.00 |
| loan_interest | Revenue from loan interest | 800000.00 |
| budget_amount | Budgeted costs | 900000.00 |
| actual_amount | Actual costs incurred | 950000.00 |
| variance_amount | Cost variance | 50000.00 |
| variance_pct | Cost variance % | 0.0556 |
| profit | Net profit | 300000.00 |
| profit_margin | Profit as % of revenue | 0.24 |
| budgeted_profit | Expected profit | 350000.00 |
| profit_variance | Profit variance | -50000.00 |
| profit_variance_pct | Profit variance % | -0.1429 |

---

### portfolio_risk_summary.csv

Aggregated portfolio risk metrics.

| Field Name | Description | Example |
|------------|-------------|---------|
| metric | Name of metric | Total Loans |
| value | Metric value | 5000 |

**Key Metrics Included**:
- Total Loans
- Total EAD
- Weighted Average PD
- Weighted Average LGD
- Total ECL
- ECL / EAD Ratio
- Delinquency Rate
- Default Rate

---

### cost_leakage_flags.csv

Cost entries with significant budget overruns.

| Field Name | Description | Example |
|------------|-------------|---------|
| cost_id | Reference to cost entry | 123 |
| cost_date | Date of cost | 2024-01-15 |
| business_unit | Business unit | Technology |
| cost_category | Category | Personnel |
| vendor | Vendor name | Acme Corp |
| budget_amount | Budget | 50000.00 |
| actual_amount | Actual spend | 65000.00 |
| variance_amount | Overrun amount | 15000.00 |
| variance_pct | Overrun percentage | 0.30 |
| severity | Severity classification | High |

**Severity Levels**:
- Moderate: 20-30% overrun
- High: 30-50% overrun
- Critical: >50% overrun

---

### scenario_results.csv

Results of stress testing scenarios.

| Field Name | Description | Example |
|------------|-------------|---------|
| scenario | Scenario name | Mild Stress |
| base_ecl | ECL under base case | 5000000.00 |
| stressed_ecl | ECL under stress | 6250000.00 |
| ecl_change | Change in ECL | 1250000.00 |
| ecl_change_pct | % change in ECL | 0.25 |
| base_pd | Base weighted PD | 0.0350 |
| stressed_pd | Stressed weighted PD | 0.0438 |
| pd_change | Change in PD | 0.0088 |
| pd_change_pct | % change in PD | 0.25 |
| base_monthly_profit | Base monthly profit | 300000.00 |
| stressed_monthly_profit | Stressed profit | 195833.33 |
| monthly_profit_change | Change in profit | -104166.67 |
| monthly_profit_change_pct | % change in profit | -0.3472 |
| total_ead | Total EAD | 500000000.00 |

---

### anomalies.csv

Detected anomalies across costs and loans.

| Field Name | Description | Example |
|------------|-------------|---------|
| cost_id / loan_id | Reference ID | 456 |
| business_unit / loan_type | Category | Technology |
| anomaly_type | Type of anomaly | High Variance |
| severity | Z-score severity | 4.25 |
| category | Cost or Loan | Cost |

---

## Data Types Reference

| Type | Description | Example Values |
|------|-------------|----------------|
| INTEGER | Whole numbers | 123, 5000, -10 |
| NUMERIC(p,s) | Decimal numbers | 1234.56, 0.0123 |
| VARCHAR(n) | Variable text, max n chars | "John Smith" |
| DATE | Calendar date | 2024-01-15 |
| TEXT | Unlimited text | Long descriptions |

**Precision Notation**:
- NUMERIC(15,2): 15 total digits, 2 after decimal (e.g., 1234567890123.45)
- NUMERIC(8,4): 8 total digits, 4 after decimal (e.g., 1234.5678)
- NUMERIC(5,2): 5 total digits, 2 after decimal (e.g., 123.45)

---

## Naming Conventions

### Table Names
- Lowercase with underscores
- Prefix indicates schema: `raw.table_name`

### Column Names
- Lowercase with underscores
- Descriptive, full words (no abbreviations unless standard)
- Foreign keys match referenced column: `customer_id`

### ID Fields
- Primary keys: `table_name_id`
- Always INTEGER type
- Always NOT NULL

---

## Data Lineage

```
Source CSVs
    ↓
raw schema (landing zone)
    ↓
analytics modules
    ↓
output CSV files
```

---

*Last Updated: January 2026*
