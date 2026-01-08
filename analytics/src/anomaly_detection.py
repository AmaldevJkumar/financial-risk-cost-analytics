"""
Anomaly Detection Module
Detects statistical outliers in cost and risk metrics
"""

import pandas as pd
import numpy as np
from scipy import stats
from .utils import calculate_z_score, save_output, AnalyticsLogger

logger = AnalyticsLogger("AnomalyDetection")

# Configuration
Z_SCORE_THRESHOLD = 3.0  # Standard deviations for anomaly


def detect_cost_anomalies(costs_df: pd.DataFrame, threshold: float = Z_SCORE_THRESHOLD) -> pd.DataFrame:
    """
    Detect anomalies in cost data using z-score.
    
    Args:
        costs_df: Costs DataFrame
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        DataFrame with detected anomalies
    """
    logger.info(f"Detecting cost anomalies (z-score > {threshold})...")
    
    # Calculate z-scores for variance
    costs_df['variance_z_score'] = calculate_z_score(costs_df['variance_pct'])
    
    # Calculate z-scores for absolute amounts
    costs_df['actual_z_score'] = calculate_z_score(costs_df['actual_amount'])
    
    # Flag anomalies
    anomalies = costs_df[
        (costs_df['variance_z_score'].abs() > threshold) |
        (costs_df['actual_z_score'].abs() > threshold)
    ].copy()
    
    # Add anomaly type
    anomalies['anomaly_type'] = anomalies.apply(
        lambda x: 'High Variance' if abs(x['variance_z_score']) > threshold else 'High Amount',
        axis=1
    )
    
    # Add severity
    anomalies['severity'] = anomalies[['variance_z_score', 'actual_z_score']].abs().max(axis=1)
    
    # Sort by severity
    anomalies = anomalies.sort_values('severity', ascending=False)
    
    logger.success(f"Detected {len(anomalies)} cost anomalies")
    return anomalies


def detect_loan_anomalies(loans_df: pd.DataFrame, threshold: float = Z_SCORE_THRESHOLD) -> pd.DataFrame:
    """
    Detect anomalies in loan portfolio.
    
    Args:
        loans_df: Loans DataFrame
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        DataFrame with detected loan anomalies
    """
    logger.info(f"Detecting loan anomalies (z-score > {threshold})...")
    
    # Calculate z-scores
    loans_df['pd_z_score'] = calculate_z_score(loans_df['pd'])
    loans_df['ecl_z_score'] = calculate_z_score(loans_df['ecl'])
    loans_df['ead_z_score'] = calculate_z_score(loans_df['ead'])
    
    # Flag anomalies
    anomalies = loans_df[
        (loans_df['pd_z_score'].abs() > threshold) |
        (loans_df['ecl_z_score'].abs() > threshold) |
        (loans_df['ead_z_score'].abs() > threshold)
    ].copy()
    
    # Add anomaly type
    anomalies['anomaly_type'] = anomalies.apply(
        lambda x: 'High PD' if abs(x['pd_z_score']) > threshold 
        else ('High ECL' if abs(x['ecl_z_score']) > threshold else 'High EAD'),
        axis=1
    )
    
    # Add severity
    anomalies['severity'] = anomalies[['pd_z_score', 'ecl_z_score', 'ead_z_score']].abs().max(axis=1)
    
    # Sort by severity
    anomalies = anomalies.sort_values('severity', ascending=False)
    
    logger.success(f"Detected {len(anomalies)} loan anomalies")
    return anomalies


def detect_time_series_anomalies(df: pd.DataFrame, value_col: str, date_col: str = 'month') -> pd.DataFrame:
    """
    Detect anomalies in time series data using rolling statistics.
    
    Args:
        df: DataFrame with time series data
        value_col: Name of value column to analyze
        date_col: Name of date column
        
    Returns:
        DataFrame with time series anomalies
    """
    logger.info(f"Detecting time series anomalies in {value_col}...")
    
    # Sort by date
    df = df.sort_values(date_col).copy()
    
    # Calculate rolling mean and std
    window = min(3, len(df) - 1)  # Use 3-month window or less if not enough data
    if window < 2:
        logger.info(f"Not enough data for rolling window (need at least 3 points)")
        return pd.DataFrame()
    
    df['rolling_mean'] = df[value_col].rolling(window=window, center=False).mean()
    df['rolling_std'] = df[value_col].rolling(window=window, center=False).std()
    
    # Calculate z-score from rolling stats
    df['rolling_z_score'] = (df[value_col] - df['rolling_mean']) / df['rolling_std']
    
    # Flag anomalies (excluding first few points where rolling stats not available)
    anomalies = df[df['rolling_z_score'].abs() > Z_SCORE_THRESHOLD].copy()
    
    logger.success(f"Detected {len(anomalies)} time series anomalies")
    return anomalies


def analyze_monthly_kpi_anomalies(monthly_kpis: pd.DataFrame) -> pd.DataFrame:
    """
    Detect anomalies in monthly KPIs.
    
    Args:
        monthly_kpis: Monthly KPIs DataFrame
        
    Returns:
        DataFrame with KPI anomalies
    """
    logger.info("Analyzing monthly KPI anomalies...")
    
    anomalies = []
    
    # Check each KPI
    kpi_columns = ['total_revenue', 'actual_amount', 'profit', 'variance_pct']
    
    for col in kpi_columns:
        if col in monthly_kpis.columns:
            col_anomalies = detect_time_series_anomalies(monthly_kpis, col, 'month')
            
            if len(col_anomalies) > 0:
                col_anomalies['kpi_name'] = col
                anomalies.append(col_anomalies[['month', 'kpi_name', col, 'rolling_z_score']])
    
    if anomalies:
        result = pd.concat(anomalies, ignore_index=True)
        logger.success(f"Detected {len(result)} KPI anomalies")
        return result
    else:
        logger.info("No KPI anomalies detected")
        return pd.DataFrame()


def generate_anomaly_report(costs_df: pd.DataFrame, loans_df: pd.DataFrame, 
                           monthly_kpis: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive anomaly report.
    
    Args:
        costs_df: Costs DataFrame
        loans_df: Loans DataFrame
        monthly_kpis: Monthly KPIs DataFrame
        
    Returns:
        Combined anomaly report
    """
    logger.section("Generating Anomaly Report")
    
    # Detect anomalies
    cost_anomalies = detect_cost_anomalies(costs_df)
    loan_anomalies = detect_loan_anomalies(loans_df)
    kpi_anomalies = analyze_monthly_kpi_anomalies(monthly_kpis)
    
    # Combine into summary
    summary = []
    
    # Cost anomalies summary
    if len(cost_anomalies) > 0:
        summary.append({
            'category': 'Costs',
            'anomaly_count': len(cost_anomalies),
            'top_issue': cost_anomalies.iloc[0]['business_unit'] if len(cost_anomalies) > 0 else 'N/A',
            'max_severity': cost_anomalies['severity'].max(),
            'total_variance': cost_anomalies['variance_amount'].sum()
        })
    
    # Loan anomalies summary
    if len(loan_anomalies) > 0:
        summary.append({
            'category': 'Loans',
            'anomaly_count': len(loan_anomalies),
            'top_issue': loan_anomalies.iloc[0]['loan_type'] if len(loan_anomalies) > 0 else 'N/A',
            'max_severity': loan_anomalies['severity'].max(),
            'total_variance': loan_anomalies['ecl'].sum()
        })
    
    # KPI anomalies summary
    if len(kpi_anomalies) > 0:
        summary.append({
            'category': 'KPIs',
            'anomaly_count': len(kpi_anomalies),
            'top_issue': kpi_anomalies.iloc[0]['kpi_name'] if len(kpi_anomalies) > 0 else 'N/A',
            'max_severity': kpi_anomalies['rolling_z_score'].abs().max(),
            'total_variance': 0
        })
    
    summary_df = pd.DataFrame(summary)
    
    # Print summary
    logger.info("\nAnomaly Detection Summary:")
    logger.info(f"  Cost Anomalies: {len(cost_anomalies)}")
    logger.info(f"  Loan Anomalies: {len(loan_anomalies)}")
    logger.info(f"  KPI Anomalies: {len(kpi_anomalies)}")
    logger.info(f"  Total Anomalies: {len(cost_anomalies) + len(loan_anomalies) + len(kpi_anomalies)}")
    
    return summary_df


def run(data: dict, monthly_kpis: pd.DataFrame):
    """
    Main execution function.
    
    Args:
        data: Dictionary with DataFrames (costs, loans)
        monthly_kpis: Monthly KPIs DataFrame
    """
    # Generate anomaly report
    summary = generate_anomaly_report(
        data['costs'],
        data['loans'],
        monthly_kpis
    )
    
    # Detect and save detailed anomalies
    cost_anomalies = detect_cost_anomalies(data['costs'])
    loan_anomalies = detect_loan_anomalies(data['loans'])
    kpi_anomalies = analyze_monthly_kpi_anomalies(monthly_kpis)
    
    # Save outputs
    save_output(summary, 'anomalies_summary.csv')
    save_output(cost_anomalies, 'cost_anomalies.csv')
    save_output(loan_anomalies, 'loan_anomalies.csv')
    
    if len(kpi_anomalies) > 0:
        save_output(kpi_anomalies, 'kpi_anomalies.csv')
    
    # Create combined anomalies file
    combined = []
    
    if len(cost_anomalies) > 0:
        cost_summary = cost_anomalies[['cost_id', 'business_unit', 'anomaly_type', 'severity']].head(10)
        cost_summary['category'] = 'Cost'
        combined.append(cost_summary)
    
    if len(loan_anomalies) > 0:
        loan_summary = loan_anomalies[['loan_id', 'loan_type', 'anomaly_type', 'severity']].head(10)
        loan_summary['category'] = 'Loan'
        combined.append(loan_summary)
    
    if combined:
        combined_df = pd.concat(combined, ignore_index=True)
        save_output(combined_df, 'anomalies.csv')
    
    return summary
