# 🏦 Financial Risk & Cost Intelligence Platform

A comprehensive banking analytics platform for risk assessment, cost optimization, and scenario analysis. Built with production-grade code architecture and realistic synthetic data generation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-12+-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

This platform provides:
- **Synthetic Data Generation**: Realistic banking datasets with referential integrity
- **Credit Risk Analytics**: PD, LGD, EAD, ECL calculations and portfolio analysis
- **Cost Intelligence**: Budget variance tracking and leakage detection
- **Scenario Analysis**: Stress testing under various economic conditions
- **Anomaly Detection**: Statistical outlier identification in costs and risks

## 🏗️ Architecture

```
┌─────────────────┐
│  Data Generator │ → CSV Files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │ ← SQL Scripts
│   Data Warehouse│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Analytics   │ → Insights & Reports
│     Modules     │
└─────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Setup Steps

```bash
# Clone repository
git clone https://github.com/yourusername/financial-risk-platform.git
cd financial-risk-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### 1. Generate Synthetic Data

```bash
cd data_generation
python generate_datasets.py
```

**Outputs** (in `data_generation/output/`):
- `customers.csv` - 10,000 customer records
- `accounts.csv` - 15,000 account records
- `loans.csv` - 5,000 loan records with risk parameters
- `transactions.csv` - 100,000 transaction records
- `costs.csv` - 1,000 cost entries with budget data
- `macro.csv` - 24 months of macroeconomic indicators

### 2. Setup Data Warehouse

```bash
# Create database
createdb financial_risk_db

# Run setup scripts
psql -d financial_risk_db -f warehouse/01_create_schemas.sql
psql -d financial_risk_db -f warehouse/02_create_tables.sql

# Update paths in 03_load_data.sql, then:
psql -d financial_risk_db -f warehouse/03_load_data.sql
```

### 3. Run Analytics

Update database credentials in `analytics/src/utils.py`, then:

```bash
cd analytics
python run_analytics.py
```

**Outputs** (in `analytics/outputs/`):
- `monthly_kpis.csv` - Revenue, costs, profit, variance
- `portfolio_risk_summary.csv` - EAD, PD, LGD, ECL metrics
- `cost_leakage_flags.csv` - Budget overruns >20%
- `scenario_results.csv` - Stress test results
- `anomalies.csv` - Statistical outliers

## 📊 Key Metrics

### Credit Risk
- **PD (Probability of Default)**: Likelihood of loan default
- **LGD (Loss Given Default)**: Expected loss severity
- **EAD (Exposure at Default)**: Outstanding amount at default
- **ECL (Expected Credit Loss)**: PD × LGD × EAD

### Financial Performance
- **Revenue**: Transaction fees + interest income
- **Costs**: Operating expenses vs budget
- **Profit**: Revenue - Costs
- **Variance**: (Actual - Budget) / Budget

### Risk Indicators
- **Delinquency Rate**: % of loans 30+ days past due
- **Default Rate**: % of loans in default status
- **Portfolio Risk**: Aggregate ECL / Total EAD

## 🧪 Scenario Analysis

Three stress scenarios:
1. **Base**: Current conditions
2. **Mild Stress**: +25% PD increase
3. **Severe Stress**: +50% PD increase

Measures impact on:
- Expected Credit Loss (ECL)
- Monthly Profit
- Portfolio risk levels

## 📚 Documentation

- **[Metric Definitions](docs/metric_definitions.md)**: Formulas and calculations
- **[Data Dictionary](docs/data_dictionary.md)**: Field-level documentation
- **[Executive Report Template](insights/exec_monthly_report.md)**: Monthly reporting
- **[Cost Actions Playbook](insights/cost_actions_playbook.md)**: Optimization framework

## 🔧 Configuration

### Database Connection
Edit `analytics/src/utils.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'financial_risk_db',
    'user': 'your_username',
    'password': 'your_password'
}
```

### Analysis Parameters
- **Leakage Threshold**: 20% in `cost_variance.py`
- **Anomaly Z-Score**: 3.0 in `anomaly_detection.py`
- **Stress Factors**: Customizable in `scenario_analysis.py`

## 📁 Project Structure

```
financial-risk-platform/
├── data_generation/       # Synthetic data scripts
├── warehouse/            # PostgreSQL setup scripts
├── analytics/            # Analysis modules
│   ├── src/             # Core analytics code
│   └── outputs/         # Generated reports
├── docs/                # Documentation
└── insights/            # Business insights
```

## 🤝 Contributing

This is a demonstration project. For production deployment:
1. Add comprehensive unit tests
2. Implement robust logging
3. Add data quality validations
4. Create CI/CD pipeline
5. Implement API layer

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built for banking data analysts and risk management professionals. Uses industry-standard risk metrics and analytical frameworks.

## 📞 Contact

For questions or suggestions, please open an issue on GitHub.

---

**⚠️ Disclaimer**: This platform uses synthetic data for demonstration purposes. Not intended for production use without proper security review and compliance validation.
