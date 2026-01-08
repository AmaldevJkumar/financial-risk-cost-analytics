"""
Utility functions for analytics modules
"""

import psycopg2
import pandas as pd
from typing import Optional, Dict, Any
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'financial_risk_db',
    'user': 'postgres',  # UPDATE THIS
    'password': 'your_password'  # UPDATE THIS
}

# Output directory
OUTPUT_DIR = 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_connection():
    """
    Create and return a database connection.
    
    Returns:
        psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


def execute_query(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as DataFrame.
    
    Args:
        query: SQL query string
        params: Optional tuple of parameters for parameterized queries
        
    Returns:
        pandas DataFrame with query results
    """
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        conn.close()


def save_output(df: pd.DataFrame, filename: str, index: bool = False):
    """
    Save DataFrame to CSV in outputs directory.
    
    Args:
        df: DataFrame to save
        filename: Output filename (without path)
        index: Whether to include index in output
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=index)
    print(f"✓ Saved: {filepath}")


def format_currency(value: float) -> str:
    """Format number as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format number as percentage."""
    return f"{value * 100:.{decimals}f}%"


def calculate_variance(actual: float, budget: float) -> Dict[str, float]:
    """
    Calculate variance metrics.
    
    Args:
        actual: Actual value
        budget: Budget/target value
        
    Returns:
        Dictionary with variance_amount and variance_pct
    """
    variance_amount = actual - budget
    variance_pct = (variance_amount / budget) if budget != 0 else 0
    
    return {
        'variance_amount': variance_amount,
        'variance_pct': variance_pct
    }


def add_month_column(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Add month column from date column.
    
    Args:
        df: DataFrame with date column
        date_col: Name of date column
        
    Returns:
        DataFrame with added 'month' column
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['month'] = df[date_col].dt.to_period('M').astype(str)
    return df


def aggregate_by_month(df: pd.DataFrame, date_col: str, agg_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Aggregate data by month.
    
    Args:
        df: DataFrame to aggregate
        date_col: Name of date column
        agg_dict: Dictionary of aggregation functions
        
    Returns:
        Aggregated DataFrame
    """
    df = add_month_column(df, date_col)
    return df.groupby('month').agg(agg_dict).reset_index()


def print_summary_stats(df: pd.DataFrame, title: str):
    """
    Print summary statistics for a DataFrame.
    
    Args:
        df: DataFrame to summarize
        title: Title for the summary
    """
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")
    print(f"{'='*60}\n")


def validate_dataframe(df: pd.DataFrame, required_columns: list, name: str) -> bool:
    """
    Validate DataFrame has required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        name: Name of DataFrame for error messages
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")
    return True


def calculate_z_score(series: pd.Series) -> pd.Series:
    """
    Calculate z-scores for a series.
    
    Args:
        series: pandas Series
        
    Returns:
        Series of z-scores
    """
    mean = series.mean()
    std = series.std()
    if std == 0:
        return pd.Series(0, index=series.index)
    return (series - mean) / std


class AnalyticsLogger:
    """Simple logger for analytics operations."""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        
    def info(self, message: str):
        print(f"[{self.module_name}] {message}")
        
    def success(self, message: str):
        print(f"[{self.module_name}] ✓ {message}")
        
    def error(self, message: str):
        print(f"[{self.module_name}] ✗ ERROR: {message}")
        
    def section(self, title: str):
        print(f"\n{'='*60}")
        print(f"[{self.module_name}] {title}")
        print(f"{'='*60}\n")
