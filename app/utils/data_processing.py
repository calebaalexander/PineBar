import pandas as pd
import numpy as np
from datetime import datetime

def load_data(file_path):
    """
    Load and process data from CSV files
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    pandas.DataFrame: Processed dataframe
    """
    try:
        df = pd.read_csv(file_path)
        # Perform any necessary data cleaning
        # Convert string columns to numeric if needed
        numeric_cols = ['Total Amount', 'Total Quantity', 'Transaction Amount', 'Transaction Count']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        # Add profit calculation if not present
        if 'Profit' not in df.columns and 'Cost' in df.columns and 'Transaction Amount' in df.columns:
            df['Profit'] = df['Transaction Amount'] - df['Cost']
            
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def filter_data(df, categories=None, start_date=None, end_date=None):
    """
    Filter dataframe based on categories and date range
    
    Parameters:
    df (pandas.DataFrame): Input dataframe
    categories (list): List of categories to include
    start_date (datetime): Start date for filtering
    end_date (datetime): End date for filtering
    
    Returns:
    pandas.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()
    
    if categories is not None and len(categories) > 0 and 'All' not in categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
    
    # Add date filtering if your data includes date columns
    
    return filtered_df

def aggregate_data(df, group_by, metrics):
    """
    Aggregate data by specified grouping and metrics
    
    Parameters:
    df (pandas.DataFrame): Input dataframe
    group_by (str or list): Column(s) to group by
    metrics (dict): Dictionary mapping output column names to aggregation functions
    
    Returns:
    pandas.DataFrame: Aggregated dataframe
    """
    return df.groupby(group_by).agg(metrics).reset_index()
