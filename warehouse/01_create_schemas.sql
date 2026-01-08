-- =====================================================
-- Financial Risk & Cost Intelligence Platform
-- Schema Creation Script
-- =====================================================

-- Drop schemas if they exist (for clean rebuild)
DROP SCHEMA IF EXISTS raw CASCADE;
DROP SCHEMA IF EXISTS analytics CASCADE;

-- Create schemas
CREATE SCHEMA raw;
CREATE SCHEMA analytics;

-- Add comments
COMMENT ON SCHEMA raw IS 'Raw data layer - landing zone for source data';
COMMENT ON SCHEMA analytics IS 'Analytics layer - curated tables and aggregations';

-- Grant permissions (adjust for your environment)
-- GRANT USAGE ON SCHEMA raw TO your_user;
-- GRANT USAGE ON SCHEMA analytics TO your_user;
-- GRANT ALL ON ALL TABLES IN SCHEMA raw TO your_user;
-- GRANT ALL ON ALL TABLES IN SCHEMA analytics TO your_user;

\echo 'Schemas created successfully!'
\echo 'Next: Run 02_create_tables.sql'
