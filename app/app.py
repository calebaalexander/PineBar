import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import os

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

# Function to load data
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Add a Category column based on SKU
        categories = {
            "BEER": ["Hemlock", "CURRENT CAN", "GANSETT", "N/A BEER", "Return Beer", "SIX POINT", "Vermonter Cider"],
            "COCKTAILS": ["BEAD & FEATHER", "BLACK MANHATTAN", "CARPETBAGGER", "COCKTAIL OF THE DAY", 
                         "COCKTAIL SHAKEN", "COCKTAIL STIRRED", "Daiquiri", "Gershwin", "Gimlet", 
                         "Gin & Sin", "HAITIAN DIVORCE", "HOT DRINX", "Manhattan", "Margarita", 
                         "Martini Gin", "Martini Vodka", "Negroni", "Old Fashioned", "Open Cocktail", 
                         "Paper Plane", "Penicillin", "Pineapple Daiq", "pineapple daiquiri", 
                         "POP-UP COCKTAIL", "Rainy Day Dark And Stormy", "SAZERAC COCKTAIL", 
                         "SHOOTER", "Soda", "SPRITZ", "TITOS MARTINI", "TONE POLICE"],
            "FOOD": ["BABA GHANO0USH", "BEEF TARTARE", "BITTER SALAD", "BOQUERONES", "BROWNIE", 
                    "Burger", "CARROTS", "CAVIAR DOG", "CHARRED BEETS", "CHICKEM KEBAB", 
                    "CHX SANDWICH", "CROQUETTES", "Doggie", "DUCK RILLETTES", "EXTRA FOCACCIA", 
                    "Extra Patty", "FALAFEL", "FOCACCIA", "FRENCH FRIES", "Fries", "HANDER STEAK", 
                    "HUMMUS", "LAMB KABAB", "LEEK TOAST", "MEZE PLATTER", "MEZE PLATTY", "PLATTY", 
                    "MOUSSE", "MOZZ STICKS", "MUHAMMARA", "NYE TACOS", "OLIVES AND PICKELS", 
                    "Open Food", "Order note", "Pimento Cheese", "Salad", "SAUSAGE", "SEA TROUT", 
                    "Smash - Vegan Patty", "STEAK FRITES", "SUNCHOKES", "TOSTADA", "TZATZIKI", "VCC"],
            "SPIRITS": ["AMARGO VALLET", "Amaro", "Balvenie", "Bourbon", "BW WHEAT", "CAMPARI", 
                       "CASCUIN TAHONA", "CURRENT CASSIS", "CYNAR", "EL DORADO 12", "ESPOLON", 
                       "Fernet", "Gin", "Hendricks", "Juice", "Macallan 18", "Makers", "Mezcal", 
                       "Michters", "MONTENEGRO", "NONINO", "OLD FORESTER 100", "Open Spirit", 
                       "Rare Breed", "RITTENHOUSE", "Rum", "SAZERAC", "Scotch", "SHOT 4$", 
                       "SHOT 5$", "SHOT 6$", "SHOT 7$", "SHOT 8$", "SHOT 9$", "Spirit", 
                       "SUZE", "Talisker", "Tequila", "TEREMANA REPOSADO", "Tesoro", "Titos", 
                       "Toki", "TULLY", "Vodka", "Wathen's", "ZACAPA"],
            "WINE": ["BTL Fizzy", "GLS Fizzy", "GLS Red", "GLS Rose", "GLS White", "OPEN WINE"],
            "N/A": ["Ginger Beer", "Mock Turtleneck", "POP-UP MOCKTAIL"],
            "Merch": ["Candle 2 oz", "Candle 9oz", "Misc", "GIFT CERTIFICATE"]
        }
        
        # Create a dictionary mapping each SKU to its category
        sku_to_category = {}
        for category, items in categories.items():
            for item in items:
                sku_to_category[item] = category
        
        # Add Category column based on SKU lookup
        df['Category'] = df['SKU'].map(sku_to_category)
        
        # Calculate Cost and Profit (if not already in the data)
        if 'Cost' not in df.columns:
            # Assume cost is 30-60% of Transaction Amount, varying by category
            cost_factors = {
                'BEER': 0.4,
                'COCKTAILS': 0.3,
                'FOOD': 0.5,
                'SPIRITS': 0.45,
                'WINE': 0.35,
                'N/A': 0.25,
                'Merch': 0.6
            }
            
            # Apply cost factor based on category
            df['Cost'] = df.apply(lambda row: row['Transaction Amount'] * cost_factors.get(row['Category'], 0.4), axis=1)
            
            # Add some randomness to make it more realistic
            df['Cost'] = df['Cost'] * (0.9 + np.random.random(len(df)) * 0.2)
        
        if 'Profit' not in df.columns:
            df['Profit'] = df['Transaction Amount'] - df['Cost']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Main application header
st.markdown("<h1 class='main-header'>Pine Bar Analytics Dashboard</h1>", unsafe_allow_html=True)

# Sidebar for navigation and filters
st.sidebar.title("Dashboard Controls")

# Data selection
data_option = st.sidebar.selectbox(
    "Select Data Period",
    ["2023 Full Year", "2024 Full Year", "2025 (up to March 5)", "All Time Comparison"]
)

# Data file mapping
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
    ["Overview", "Sales Analysis", "Profitability Analysis", "Category Performance", "Product Performance", "Trend Analysis"]
)

# Metric sorting options
metric_sort = st.sidebar.selectbox(
    "Sort Products By",
    ["Most Sales", "Least Sales", "Most Profit", "Least Profit", "Highest Margin", "Lowest Margin", "Most Orders", "Least Orders"]
)

# Time granularity for trend analysis
if analysis_type == "Trend Analysis":
    time_granularity = st.sidebar.selectbox(
        "Time Granularity",
        ["Monthly", "Quarterly", "Yearly"]
    )

# Load data based on selection
if data_option == "All Time Comparison":
    # Load all datasets
    df_2023 = load_data(data_files["2023 Full Year"])
    df_2024 = load_data(data_files["2024 Full Year"])
    df_2025 = load_data(data_files["2025 (up to March 5)"])
    
    # Add year column to each dataset
    df_2023['Year'] = '2023'
    df_2024['Year'] = '2024'
    df_2025['Year'] = '2025'
    
    # Add date ranges
    df_2023['Date_Range'] = pd.date_range(start='2023-05-12', periods=len(df_2023), freq='D')
    df_2024['Date_Range'] = pd.date_range(start='2024-01-01', periods=len(df_2024), freq='D')
    df_2025['Date_Range'] = pd.date_range(start='2025-01-01', periods=len(df_2025), freq='D')
    
    # Combine datasets
    df = pd.concat([df_2023, df_2024, df_2025])
else:
    df = load_data(data_files[data_option])
    
    # Add year column
    if data_option == "2023 Full Year":
        df['Year'] = '2023'
        df['Date_Range'] = pd.date_range(start='2023-05-12', periods=len(df), freq='D')
    elif data_option == "2024 Full Year":
        df['Year'] = '2024'
        df['Date_Range'] = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
    else:
        df['Year'] = '2025'
        df['Date_Range'] = pd.date_range(start='2025-01-01', periods=len(df), freq='D')

# Apply category filter
if "All" not in category_filter:
    df = df[df['Category'].isin(category_filter)]

# Function to create metrics row
def create_metrics_row(df):
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${df['Transaction Amount'].sum():,.0f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Revenue</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${df['Profit'].sum():,.0f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Profit</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{df['Transaction Count'].sum():,.0f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Orders</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        profit_margin = (df['Profit'].sum() / df['Transaction Amount'].sum() * 100) if df['Transaction Amount'].sum() > 0 else 0
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{profit_margin:.1f}%</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Overall Margin</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col5:
        avg_order = df['Transaction Amount'].sum() / df['Transaction Count'].sum() if df['Transaction Count'].sum() > 0 else 0
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${avg_order:.2f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Avg Order Value</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Function to create category breakdown
def create_category_breakdown(df):
    # Group by category
    category_sales = df.groupby('Category').agg({
        'Transaction Amount': 'sum',
        'Transaction Count': 'sum',
        'Profit': 'sum',
        'Cost': 'sum'
    }).reset_index()
    
    # Calculate profit margin percentage for each category
    category_sales['Profit Margin'] = (category_sales['Profit'] / category_sales['Transaction Amount'] * 100).round(1)
    
    # Sort by Transaction Amount
    category_sales = category_sales.sort_values('Transaction Amount', ascending=False)
    
    # Create pie chart for category sales
    fig1 = px.pie(
        category_sales, 
        values='Transaction Amount', 
        names='Category',
        title='Revenue by Category',
        color_discrete_sequence=px.colors.qualitative.Bold,
        hole=0.4
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    
    # Create horizontal bar chart for category profit
    fig2 = px.bar(
        category_sales.sort_values('Profit', ascending=True),
        x='Profit',
        y='Category',
        title='Profit by Category',
        orientation='h',
        color='Profit Margin',
        color_continuous_scale='Viridis',
        text=category_sales.sort_values('Profit', ascending=True)['Profit'].apply(lambda x: f"${x:,.0f}")
    )
    fig2.update_traces(textposition='outside')
    
    # Display charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # Category metrics
    st.markdown("<h3 class='sub-header'>Category Performance Metrics</h3>", unsafe_allow_html=True)
    
    # Format the DataFrame for display
    display_df = category_sales.copy()
    display_df['Revenue'] = display_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
    display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
    display_df['Margin'] = display_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
    display_df['Orders'] = display_df['Transaction Count'].apply(lambda x: f"{x:,.0f}")
    display_df['Avg Order Value'] = (display_df['Transaction Amount'] / display_df['Transaction Count']).apply(lambda x: f"${x:.2f}")
    
    # Display the formatted DataFrame
    st.dataframe(display_df[['Category', 'Revenue', 'Profit', 'Margin', 'Orders', 'Avg Order Value']], use_container_width=True)

# Function to create product performance analysis
def create_product_performance(df, metric_sort):
    st.markdown("<h2 class='sub-header'>Product Performance</h2>", unsafe_allow_html=True)
    
    # Add profit margin column if not present
    if 'Profit Margin' not in df.columns:
        df['Profit Margin'] = (df['Profit'] / df['Transaction Amount'] * 100)
    
    # Determine sorting based on selected option
    if metric_sort == "Most Sales":
        df_sorted = df.sort_values('Transaction Amount', ascending=False).head(10)
        metric = 'Transaction Amount'
        title = 'Top 10 Products by Sales'
        color_values = 'Category'
    elif metric_sort == "Least Sales":
        df_sorted = df.sort_values('Transaction Amount', ascending=True).head(10)
        metric = 'Transaction Amount'
        title = 'Bottom 10 Products by Sales'
        color_values = 'Category'
    elif metric_sort == "Most Profit":
        df_sorted = df.sort_values('Profit', ascending=False).head(10)
        metric = 'Profit'
        title = 'Top 10 Products by Profit'
        color_values = 'Category'
    elif metric_sort == "Least Profit":
        df_sorted = df.sort_values('Profit', ascending=True).head(10)
        metric = 'Profit'
        title = 'Bottom 10 Products by Profit'
        color_values = 'Category'
    elif metric_sort == "Highest Margin":
        df_sorted = df.sort_values('Profit Margin', ascending=False).head(10)
        metric = 'Profit Margin'
        title = 'Top 10 Products by Profit Margin'
        color_values = 'Profit Margin'
    elif metric_sort == "Lowest Margin":
        df_sorted = df.sort_values('Profit Margin', ascending=True).head(10)
        metric = 'Profit Margin'
        title = 'Bottom 10 Products by Profit Margin'
        color_values = 'Profit Margin'
    elif metric_sort == "Most Orders":
        df_sorted = df.sort_values('Transaction Count', ascending=False).head(10)
        metric = 'Transaction Count'
        title = 'Top 10 Products by Order Count'
        color_values = 'Category'
    else:  # Least Orders
        df_sorted = df.sort_values('Transaction Count', ascending=True).head(10)
        metric = 'Transaction Count'
        title = 'Bottom 10 Products by Order Count'
        color_values = 'Category'
    
    # Create horizontal bar chart
    if metric in ['Profit Margin']:
        fig = px.bar(
            df_sorted,
            x=metric,
            y='SKU',
            title=title,
            orientation='h',
            color=color_values,
            text=df_sorted[metric].apply(lambda x: f"{x:.1f}%"),
            color_continuous_scale='Viridis' if metric == 'Profit Margin' else None,
            color_discrete_sequence=px.colors.qualitative.Bold if metric != 'Profit Margin' else None
        )
        fig.update_traces(textposition='outside')
    elif metric in ['Transaction Count']:
        fig = px.bar(
            df_sorted,
            x=metric,
            y='SKU',
            title=title,
            orientation='h',
            color=color_values,
            text=df_sorted[metric],
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(textposition='outside')
    else:
        fig = px.bar(
            df_sorted,
            x=metric,
            y='SKU',
            title=title,
            orientation='h',
            color=color_values,
            text=df_sorted[metric].apply(lambda x: f"${x:,.0f}"),
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the data table
    with st.expander("View Detailed Product Data"):
        df_sorted['Profit Margin'] = df_sorted['Profit Margin'].round(1)
        
        # Format columns for display
        display_df = df_sorted.copy()
        display_df['Revenue'] = display_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
        display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
        display_df['Margin'] = display_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
        display_df['Orders'] = display_df['Transaction Count']
        display_df['Avg Order Value'] = (display_df['Transaction Amount'] / display_df['Transaction Count']).apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df[['SKU', 'Category', 'Revenue', 'Profit', 'Margin', 'Orders', 'Avg Order Value']], use_container_width=True)

# Function to create profitability analysis
def create_profitability_analysis(df):
    st.markdown("<h2 class='sub-header'>Profitability Analysis</h2>", unsafe_allow_html=True)
    
    # Profit metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_profit = df['Profit'].sum()
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${total_profit:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Profit</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        overall_margin = (df['Profit'].sum() / df['Transaction Amount'].sum() * 100) if df['Transaction Amount'].sum() > 0 else 0
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{overall_margin:.1f}%</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Overall Profit Margin</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        profit_per_order = df['Profit'].sum() / df['Transaction Count'].sum() if df['Transaction Count'].sum() > 0 else 0
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${profit_per_order:.2f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Profit per Order</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Margin distribution analysis
    st.markdown("<h3>Profit Margin Distribution by Category</h3>")
    
    # Group by category and calculate margin statistics
    category_margins = df.groupby('Category').agg({
        'Profit Margin': ['mean', 'min', 'max', 'std'],
        'Transaction Amount': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    category_margins.columns = ['Category', 'Avg Margin', 'Min Margin', 'Max Margin', 'Margin StdDev', 'Revenue', 'Profit']
    category_margins['Overall Margin'] = (category_margins['Profit'] / category_margins['Revenue'] * 100).round(1)
    
    # Sort by overall margin
    category_margins = category_margins.sort_values('Overall Margin', ascending=False)
    
    # Create a box plot for margin distribution
    fig = go.Figure()
    
    for category in category_margins['Category']:
        category_df = df[df['Category'] == category]
        
        fig.add_trace(go.Box(
            y=category_df['Profit Margin'],
            name=category,
            boxmean=True
        ))
    
    fig.update_layout(
        title='Profit Margin Distribution by Category',
        yaxis_title='Profit Margin (%)',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display margin metrics table
    st.markdown("<h3>Category Margin Metrics</h3>")
    
    # Format for display
    display_df = category_margins.copy()
    display_df['Avg Margin'] = display_df['Avg Margin'].apply(lambda x: f"{x:.1f}%")
    display_df['Min Margin'] = display_df['Min Margin'].apply(lambda x: f"{x:.1f}%")
    display_df['Max Margin'] = display_df['Max Margin'].apply(lambda x: f"{x:.1f}%")
    display_df['Margin StdDev'] = display_df['Margin StdDev'].apply(lambda x: f"{x:.2f}")
    display_df['Overall Margin'] = display_df['Overall Margin'].apply(lambda x: f"{x:.1f}%")
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(display_df, use_container_width=True)
    
    # High vs Low margin product analysis
    st.markdown("<h3>High vs Low Margin Products</h3>")
    
    # Define high and low margin thresholds (e.g., top 10% and bottom 10%)
    high_margin_threshold = df['Profit Margin'].quantile(0.9)
    low_margin_threshold = df['Profit Margin'].quantile(0.1)
    
    high_margin_products = df[df['Profit Margin'] >= high_margin_threshold].sort_values('Profit', ascending=False).head(5)
    low_margin_products = df[df['Profit Margin'] <= low_margin_threshold].sort_values('Profit', ascending=True).head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h4>Top 5 High-Margin Products</h4>", unsafe_allow_html=True)
        
        # Format for display
        display_df = high_margin_products.copy()
        display_df['Revenue'] = display_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
        display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
        display_df['Margin'] = display_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_df[['SKU', 'Category', 'Revenue', 'Profit', 'Margin']], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h4>Bottom 5 Low-Margin Products</h4>", unsafe_allow_html=True)
        
        # Format for display
        display_df = low_margin_products.copy()
        display_df['Revenue'] = display_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
        display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
        display_df['Margin'] = display_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_df[['SKU', 'Category', 'Revenue', 'Profit', 'Margin']], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Function to create sales analysis
def create_sales_analysis(df):
    st.markdown("<h2 class='sub-header'>Sales Analysis</h2>", unsafe_allow_html=True)
    
    # Sales metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Transaction Amount'].sum()
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${total_revenue:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Revenue</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        total_orders = df['Transaction Count'].sum()
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{total_orders:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Orders</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        avg_order_value = df['Transaction Amount'].sum() / df['Transaction Count'].sum() if df['Transaction Count'].sum() > 0 else 0
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${avg_order_value:.2f}</div>", unsafe_allow_)
