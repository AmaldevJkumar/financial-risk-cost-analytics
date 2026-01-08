"""
Main Analytics Runner
Orchestrates all analytics modules
"""

import sys
from datetime import datetime

# Import analytics modules
from src import data_prep, kpi_tables, risk_metrics, cost_variance, scenario_analysis, anomaly_detection
from src.utils import AnalyticsLogger

logger = AnalyticsLogger("Main")


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print("  FINANCIAL RISK & COST INTELLIGENCE PLATFORM")
    print("  Analytics Pipeline")
    print("="*70 + "\n")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def print_summary():
    """Print completion summary."""
    print("\n" + "="*70)
    print("  ANALYTICS COMPLETE")
    print("="*70)
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nOutputs saved to: analytics/outputs/")
    print("\nGenerated Files:")
    print("  ✓ monthly_kpis.csv")
    print("  ✓ portfolio_risk_summary.csv")
    print("  ✓ risk_by_segment.csv")
    print("  ✓ risk_by_loan_type.csv")
    print("  ✓ risk_vintage_analysis.csv")
    print("  ✓ cost_leakage_flags.csv")
    print("  ✓ variance_by_business_unit.csv")
    print("  ✓ variance_by_category.csv")
    print("  ✓ variance_by_vendor.csv")
    print("  ✓ scenario_results.csv")
    print("  ✓ segment_sensitivity.csv")
    print("  ✓ anomalies_summary.csv")
    print("  ✓ cost_anomalies.csv")
    print("  ✓ loan_anomalies.csv")
    print("  ✓ anomalies.csv")
    print("\nNext Steps:")
    print("  • Review outputs in analytics/outputs/")
    print("  • Check insights/ for executive summaries")
    print("  • Refer to docs/ for metric definitions")
    print("="*70 + "\n")


def main():
    """Main execution flow."""
    try:
        print_banner()
        
        # Step 1: Load data
        logger.section("STEP 1: DATA LOADING")
        data = data_prep.load_all_data()
        
        # Step 2: Generate KPIs
        logger.section("STEP 2: KPI CALCULATION")
        monthly_kpis = kpi_tables.run(data)
        
        # Step 3: Risk metrics
        logger.section("STEP 3: RISK ANALYSIS")
        risk_summary = risk_metrics.run(data)
        
        # Step 4: Cost variance analysis
        logger.section("STEP 4: COST VARIANCE ANALYSIS")
        cost_leakages = cost_variance.run(data)
        
        # Step 5: Scenario analysis
        logger.section("STEP 5: SCENARIO ANALYSIS")
        scenario_results = scenario_analysis.run(data, monthly_kpis)
        
        # Step 6: Anomaly detection
        logger.section("STEP 6: ANOMALY DETECTION")
        anomalies = anomaly_detection.run(data, monthly_kpis)
        
        # Print summary
        print_summary()
        
        return 0
        
    except Exception as e:
        logger.error(f"Analytics pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
