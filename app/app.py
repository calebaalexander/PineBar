import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import calendar

# Import helper modules
from data_processing import generate_data
from visualizations import (
    create_metrics_row,
    create_category_breakdown,
    create_product_performance,
    create_profitability_analysis,
    create_sales_analysis,
    create_category_performance
)

# Set page config
st.set_page_config(
    page_title="Pine Bar Dashboard",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #34495e;
        margin-bottom: 0.5rem;
    }
    .card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 0.15rem 1.75rem rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
    }
    .metric-label {
        font-size: 1rem;
        text-align: center;
        color: #6c757d;
    }
    .highlight-positive {
        color: #28a745;
        font-weight: 500;
    }
    .highlight-negative {
        color: #dc3545;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Main application header
st.markdown("<h1 class='main-header'>Pine Bar Analytics Dashboard</h1>", unsafe_allow_html=True)

# Sidebar for navigation and filters
st.sidebar.title("Dashboard Controls")

# Data selection
data_option = st.sidebar.selectbox(
    "Select Data Period",
    ["2023 Full Year", "2024 Full Year", "2025 (up to March 5)", "All Time Comparison"]
)

# Data file mapping (in a real app, these would be actual files)
data_files = {
    "2023 Full Year": "hemlock_product_breakdown_20230512_20240101.csv",
    "2024 Full Year": "hemlock_product_breakdown_20240101_20250101.csv",
    "2025 (up to March 5)": "hemlock_product_breakdown_20250101_20260101.csv"
}

# Category filter for analysis
all_categories = ["BEER", "COCKTAILS", "FOOD", "SPIRITS", "WINE", "N/A", "Merch"]
category_filter = st.sidebar.multiselect(
    "Filter by Category",
    ["All"] + all_categories,
    default=["All"]
)

# Analysis type selection
analysis_type = st.sidebar.selectbox(
    "Select Analysis View",
    ["Overview", "Sales Analysis", "Profitability Analysis", "Category Performance", "Product Performance"]
)

# Metric sorting options
metric_sort = st.sidebar.selectbox(
    "Sort Products By",
    ["Most Sales", "Least Sales", "Most Profit", "Least Profit", "Highest Margin", "Lowest Margin", "Most Orders", "Least Orders"]
)

# Load data based on selection
if data_option == "All Time Comparison":
    # Load all datasets
    df_2023 = generate_data("2023 Full Year")
    df_2024 = generate_data("2024 Full Year")
    df_2025 = generate_data("2025 (up to March 5)")
    
    # Combine datasets
    df = pd.concat([df_2023, df_2024, df_2025])
else:
    df = generate_data(data_option)

# Apply category filter
if "All" not in category_filter:
    df = df[df['Category'].isin(category_filter)]

# Render the appropriate view based on selection
if analysis_type == "Overview":
    # Display key metrics
    create_metrics_row(df)
    
    # Display category breakdown
    create_category_breakdown(df)
    
    # Display top products
    create_product_performance(df, metric_sort)
    
elif analysis_type == "Sales Analysis":
    # Sales Analysis view
    create_sales_analysis(df)
    
elif analysis_type == "Profitability Analysis":
    # Profitability Analysis view
    create_profitability_analysis(df)
    
elif analysis_type == "Category Performance":
    # Category Performance view
    create_category_performance(df)
    
elif analysis_type == "Product Performance":
    # Product Performance view
    create_product_performance(df, metric_sort)
    
# Add a note at the bottom
st.markdown("---")
st.markdown("*Note: This dashboard uses synthetic data generated for demonstration purposes.*")
