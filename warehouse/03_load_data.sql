-- =====================================================
-- Financial Risk & Cost Intelligence Platform
-- Data Loading Script
-- =====================================================

-- IMPORTANT: Update the file paths below to match your local setup
-- Use ABSOLUTE PATHS for Windows (e.g., 'C:/Users/YourName/...')

-- =====================================================
-- LOAD DATA USING COPY COMMAND
-- =====================================================

-- Clear existing data
TRUNCATE TABLE raw.transactions CASCADE;
TRUNCATE TABLE raw.loans CASCADE;
TRUNCATE TABLE raw.accounts CASCADE;
TRUNCATE TABLE raw.customers CASCADE;
TRUNCATE TABLE raw.costs CASCADE;
TRUNCATE TABLE raw.macro CASCADE;

\echo 'Loading customers...'
COPY raw.customers FROM 'C:/path/to/financial-risk-platform/data_generation/output/customers.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo 'Loading accounts...'
COPY raw.accounts FROM 'C:/path/to/financial-risk-platform/data_generation/output/accounts.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo 'Loading loans...'
COPY raw.loans FROM 'C:/path/to/financial-risk-platform/data_generation/output/loans.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo 'Loading transactions...'
COPY raw.transactions FROM 'C:/path/to/financial-risk-platform/data_generation/output/transactions.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo 'Loading costs...'
COPY raw.costs FROM 'C:/path/to/financial-risk-platform/data_generation/output/costs.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

\echo 'Loading macro indicators...'
COPY raw.macro FROM 'C:/path/to/financial-risk-platform/data_generation/output/macro.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- =====================================================
-- VERIFY LOADS
-- =====================================================

\echo 'Verifying data loads...'

SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM raw.customers
UNION ALL
SELECT 'accounts', COUNT(*) FROM raw.accounts
UNION ALL
SELECT 'loans', COUNT(*) FROM raw.loans
UNION ALL
SELECT 'transactions', COUNT(*) FROM raw.transactions
UNION ALL
SELECT 'costs', COUNT(*) FROM raw.costs
UNION ALL
SELECT 'macro', COUNT(*) FROM raw.macro;

\echo 'Data loading complete!'
\echo 'Next: Run analytics (cd analytics && python run_analytics.py)'
