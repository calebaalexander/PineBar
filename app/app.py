import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Set page config
st.set_page_config(
    page_title="Pine Bar Dashboard",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for maintaining values
if 'data_period' not in st.session_state:
    st.session_state.data_period = "2025 (up to March 5)"
    
if 'selected_categories' not in st.session_state:
    st.session_state.selected_categories = ["All"]
    
if 'analysis_view' not in st.session_state:
    st.session_state.analysis_view = "Overview"
    
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = "Most Profit"

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
</style>
""", unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Main application header
st.markdown("<h1 class='main-header'>Pine Bar Analytics Dashboard</h1>", unsafe_allow_html=True)

# Callback functions for widgets
def update_data_period():
    st.session_state.data_period = st.session_state.temp_data_period
    
def update_categories():
    st.session_state.selected_categories = st.session_state.temp_categories
    
def update_analysis_view():
    st.session_state.analysis_view = st.session_state.temp_analysis_view
    
def update_sort_by():
    st.session_state.sort_by = st.session_state.temp_sort_by

# Sidebar for navigation and filters
st.sidebar.title("Dashboard Controls")

# Data selection
st.sidebar.selectbox(
    "Select Data Period",
    ["2023 Full Year", "2024 Full Year", "2025 (up to March 5)", "All Time Comparison"],
    index=["2023 Full Year", "2024 Full Year", "2025 (up to March 5)", "All Time Comparison"].index(st.session_state.data_period),
    key="temp_data_period",
    on_change=update_data_period
)

# Data file mapping
data_files = {
    "2023 Full Year": "hemlock_product_breakdown_20230512_20240101.csv",
    "2024 Full Year": "hemlock_product_breakdown_20240101_20250101.csv",
    "2025 (up to March 5)": "hemlock_product_breakdown_20250101_20260101.csv"
}

# Time range filter (for when "All Time Comparison" is selected)
if st.session_state.data_period == "All Time Comparison":
    time_range = st.sidebar.date_input(
        "Select Custom Date Range",
        value=[datetime(2023, 5, 12), datetime(2025, 3, 5)],
        min_value=datetime(2023, 5, 12),
        max_value=datetime(2025, 3, 5)
    )

# Category filter for analysis
st.sidebar.multiselect(
    "Filter by Category",
    ["All", "BEER", "COCKTAILS", "FOOD", "SPIRITS", "WINE", "N/A", "Merch"],
    default=st.session_state.selected_categories,
    key="temp_categories",
    on_change=update_categories
)

# Analysis type selection
st.sidebar.selectbox(
    "Select Analysis View",
    ["Overview", "Sales Analysis", "Profitability Analysis", "Inventory Analysis", "Customer Trends"],
    index=["Overview", "Sales Analysis", "Profitability Analysis", "Inventory Analysis", "Customer Trends"].index(st.session_state.analysis_view),
    key="temp_analysis_view",
    on_change=update_analysis_view
)

# Metric sorting options
st.sidebar.selectbox(
    "Sort Products By",
    ["Most Sales", "Least Sales", "Most Profit", "Least Profit", "Most Orders", "Least Orders"],
    index=["Most Sales", "Least Sales", "Most Profit", "Least Profit", "Most Orders", "Least Orders"].index(st.session_state.sort_by),
    key="temp_sort_by",
    on_change=update_sort_by
)

# Function to simulate data loading (in a real app, you'd load the actual files)
def get_data(option):
    try:
        # In a real implementation, this would load the actual files
        # For demo purposes, we'll create synthetic data based on the provided structure
        
        # Base dataframe structure
        columns = ["SKU", "Category", "Total Amount", "Total Quantity", "Total Transaction Count", 
                "Zero Priced Count", "Discounted Amount", "Discounted Quantity", 
                "Discounted Transaction Count", "Offered Amount", "Offered Quantity", 
                "Offered Transaction Count", "Loss Amount", "Loss Quantity", 
                "Loss Transaction Count", "Returned Amount", "Returned Quantity", 
                "Returned Transaction Count", "Transaction Amount", "Transaction Quantity", 
                "Transaction Count", "Cost", "Profit"]
        
        # Sample data for demonstration
        if option == "2023 Full Year":
            # Create more realistic 2023 data
            np.random.seed(2023)
            n_samples = 50
        elif option == "2024 Full Year":
            # Create more realistic 2024 data
            np.random.seed(2024)
            n_samples = 60
        else:  # 2025 data
            # Create more realistic 2025 data (partial year)
            np.random.seed(2025)
            n_samples = 35
        
        # Categories and their items
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
        
        # Create empty dataframe
        data = []
        
        # Generate synthetic data for each category
        for category, items in categories.items():
            for item in items:
                # Only include some items to match the number of samples
                if np.random.random() > 0.3:
                    # Generate realistic metrics
                    total_amount = max(150, np.random.randint(10, 15000))  # Ensure minimum value
                    total_quantity = np.random.randint(1, max(2, int(total_amount / 15) + 1))
                    transaction_count = np.random.randint(1, min(500, total_quantity + 1))
                    
                    # Calculate other metrics based on total
                    zero_priced = np.random.randint(0, int(total_quantity * 0.05) + 1)
                    disc_amount = -np.random.randint(0, int(total_amount * 0.25) + 1) if np.random.random() > 0.3 else 0
                    disc_quantity = np.random.randint(0, int(total_quantity * 0.15) + 1) if disc_amount < 0 else 0
                    disc_transactions = np.random.randint(0, min(50, disc_quantity + 1)) if disc_quantity > 0 else 0
                    
                    offered_amount = np.random.randint(0, int(total_amount * 0.1) + 1) if np.random.random() > 0.7 else 0
                    offered_quantity = np.random.randint(0, int(total_quantity * 0.05) + 1) if offered_amount > 0 else 0
                    offered_transactions = np.random.randint(0, min(20, offered_quantity + 1)) if offered_quantity > 0 else 0
                    
                    loss_amount = -np.random.randint(0, int(total_amount * 0.1) + 1) if np.random.random() > 0.8 else 0
                    loss_quantity = np.random.randint(0, int(total_quantity * 0.05) + 1) if loss_amount < 0 else 0
                    loss_transactions = np.random.randint(0, min(10, loss_quantity + 1)) if loss_quantity > 0 else 0
                    
                    returned_amount = -np.random.randint(0, int(total_amount * 0.05) + 1) if np.random.random() > 0.85 else 0
                    returned_quantity = np.random.randint(0, int(total_quantity * 0.03) + 1) if returned_amount < 0 else 0
                    returned_transactions = np.random.randint(0, min(5, returned_quantity + 1)) if returned_quantity > 0 else 0
                    
                    # Calculate final transaction values
                    transaction_amount = total_amount + disc_amount + offered_amount + loss_amount + returned_amount
                    transaction_quantity = total_quantity - zero_priced - disc_quantity - offered_quantity - loss_quantity - returned_quantity
                    if transaction_quantity < 0: transaction_quantity = 0
                    
                    # Cost and profit
                    cost_factor = 0.3 + np.random.random() * 0.3  # Cost between 30-60% of total
                    cost = total_amount * cost_factor
                    profit = transaction_amount - cost
                    
                    data.append([
                        item, category, total_amount, total_quantity, transaction_count,
                        zero_priced, disc_amount, disc_quantity, disc_transactions,
                        offered_amount, offered_quantity, offered_transactions,
                        loss_amount, loss_quantity, loss_transactions,
                        returned_amount, returned_quantity, returned_transactions,
                        transaction_amount, transaction_quantity, transaction_count,
                        cost, profit
                    ])
        
        df = pd.DataFrame(data, columns=columns)
        return df
    
    except Exception as e:
        st.error(f"Error generating data: {e}")
        return pd.DataFrame(columns=columns)

# Load appropriate data based on selection
try:
    if st.session_state.data_period == "All Time Comparison":
        df_2023 = get_data("2023 Full Year")
        df_2024 = get_data("2024 Full Year")
        df_2025 = get_data("2025 (up to March 5)")
        
        # Add year column to each dataset
        df_2023['Year'] = '2023'
        df_2024['Year'] = '2024'
        df_2025['Year'] = '2025'
        
        # Combine datasets
        df = pd.concat([df_2023, df_2024, df_2025])
    else:
        df = get_data(st.session_state.data_period)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Apply category filter
try:
    if "All" not in st.session_state.selected_categories:
        df = df[df['Category'].isin(st.session_state.selected_categories)]
except Exception as e:
    st.error(f"Error applying category filter: {e}")

# Function to create metrics row
def create_metrics_row(df):
    try:
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
            st.markdown("<div class='metric-label'>Total Transactions</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            profit_margin = (df['Profit'].sum() / df['Transaction Amount'].sum() * 100) if df['Transaction Amount'].sum() > 0 else 0
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{profit_margin:.1f}%</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Profit Margin</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col5:
            avg_transaction = df['Transaction Amount'].sum() / df['Transaction Count'].sum() if df['Transaction Count'].sum() > 0 else 0
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>${avg_transaction:.2f}</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Avg Transaction</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error creating metrics row: {e}")

# Function to create category breakdown
def create_category_breakdown(df):
    try:
        # Group by category
        category_sales = df.groupby('Category').agg({
            'Transaction Amount': 'sum',
            'Transaction Count': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        # Create pie chart for category sales
        fig1 = px.pie(
            category_sales, 
            values='Transaction Amount', 
            names='Category',
            title='Sales by Category',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        
        # Create horizontal bar chart for category profit
        category_sales = category_sales.sort_values('Profit', ascending=True)
        fig2 = px.bar(
            category_sales,
            x='Profit',
            y='Category',
            title='Profit by Category',
            orientation='h',
            color='Profit',
            color_continuous_scale='Viridis'
        )
        
        # Display charts
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating category breakdown: {e}")

# Function to create top products analysis
def create_top_products(df, metric_sort):
    try:
        st.markdown("<h2 class='sub-header'>Product Performance</h2>", unsafe_allow_html=True)
        
        # Determine sorting based on selected option
        if metric_sort == "Most Sales":
            df_sorted = df.sort_values('Transaction Amount', ascending=False).head(10)
            metric = 'Transaction Amount'
            title = 'Top 10 Products by Sales ($)'
        elif metric_sort == "Least Sales":
            df_sorted = df.sort_values('Transaction Amount', ascending=True).head(10)
            metric = 'Transaction Amount'
            title = 'Bottom 10 Products by Sales ($)'
        elif metric_sort == "Most Profit":
            df_sorted = df.sort_values('Profit', ascending=False).head(10)
            metric = 'Profit'
            title = 'Top 10 Products by Profit ($)'
        elif metric_sort == "Least Profit":
            df_sorted = df.sort_values('Profit', ascending=True).head(10)
            metric = 'Profit'
            title = 'Bottom 10 Products by Profit ($)'
        elif metric_sort == "Most Orders":
            df_sorted = df.sort_values('Transaction Count', ascending=False).head(10)
            metric = 'Transaction Count'
            title = 'Top 10 Products by Order Count'
        else:  # Least Orders
            df_sorted = df.sort_values('Transaction Count', ascending=True).head(10)
            metric = 'Transaction Count'
            title = 'Bottom 10 Products by Order Count'
        
        # Create horizontal bar chart
        fig = px.bar(
            df_sorted,
            x=metric,
            y='SKU',
            title=title,
            orientation='h',
            color='Category',
            text=metric if metric != 'Transaction Count' else None,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        if metric != 'Transaction Count':
            fig.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display the data table
        with st.expander("View Detailed Product Data"):
            if metric in ['Transaction Amount', 'Profit']:
                df_sorted['Profit Margin'] = (df_sorted['Profit'] / df_sorted['Transaction Amount'] * 100).round(1)
                df_display = df_sorted[['SKU', 'Category', 'Transaction Amount', 'Profit', 'Profit Margin', 'Transaction Count']]
                df_display = df_display.rename(columns={
                    'Transaction Amount': 'Revenue ($)',
                    'Profit': 'Profit ($)',
                    'Profit Margin': 'Margin (%)',
                    'Transaction Count': 'Orders'
                })
            else:
                df_display = df_sorted[['SKU', 'Category', 'Transaction Count', 'Transaction Amount', 'Profit']]
                df_display = df_display.rename(columns={
                    'Transaction Amount': 'Revenue ($)',
                    'Profit': 'Profit ($)',
                    'Transaction Count': 'Orders'
                })
            
            st.dataframe(df_display, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating top products analysis: {e}")

# Function to create time trend analysis for all-time comparison
def create_time_trends(df):
    try:
        # Create synthetic monthly data
        months = pd.date_range(start='2023-05-01', end='2025-03-01', freq='MS')
        monthly_data = []
        
        for year in df['Year'].unique():
            year_df = df[df['Year'] == year]
            total_amount = year_df['Transaction Amount'].sum()
            total_profit = year_df['Profit'].sum()
            total_transactions = year_df['Transaction Count'].sum()
            
            # Distribute across months based on year
            if year == '2023':
                valid_months = months[(months >= '2023-05-01') & (months <= '2023-12-01')]
            elif year == '2024':
                valid_months = months[(months >= '2024-01-01') & (months <= '2024-12-01')]
            else:  # 2025
                valid_months = months[(months >= '2025-01-01') & (months <= '2025-03-01')]
            
            # Create monthly distribution with seasonal variations
            n_months = len(valid_months)
            
            # Base distribution with seasonal patterns
            monthly_factors = np.ones(n_months)
            
            # Summer peak (Jun-Aug)
            summer_indices = [i for i, m in enumerate(valid_months) if m.month in [6, 7, 8]]
            for idx in summer_indices:
                monthly_factors[idx] *= 1.3
                
            # Winter holiday peak (Nov-Dec)
            holiday_indices = [i for i, m in enumerate(valid_months) if m.month in [11, 12]]
            for idx in holiday_indices:
                monthly_factors[idx] *= 1.4
                
            # January drop
            jan_indices = [i for i, m in enumerate(valid_months) if m.month == 1]
            for idx in jan_indices:
                monthly_factors[idx] *= 0.7
            
            # Normalize factors
            monthly_factors = monthly_factors / monthly_factors.sum() * n_months
            
            # Create monthly entries
            for i, month in enumerate(valid_months):
                # Add some randomness
                factor = monthly_factors[i] * (0.9 + 0.2 * np.random.random())
                
                monthly_data.append({
                    'Date': month,
                    'Year': year,
                    'Month': calendar.month_name[month.month],
                    'Revenue': total_amount / n_months * factor,
                    'Profit': total_profit / n_months * factor,
                    'Transactions': int(total_transactions / n_months * factor)
                })
        
        monthly_df = pd.DataFrame(monthly_data)
        
        # Create line charts
        fig1 = px.line(
            monthly_df, 
            x='Date', 
            y=['Revenue', 'Profit'],
            title='Monthly Revenue and Profit Trends',
            color_discrete_sequence=['#2C3E50', '#18BC9C']
        )
        
        fig2 = px.line(
            monthly_df, 
            x='Date', 
            y='Transactions',
            title='Monthly Transaction Count',
            color_discrete_sequence=['#E74C3C']
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        
        # Year-over-year comparison
        if '2024' in df['Year'].unique() and '2023' in df['Year'].unique():
            st.markdown("<h2 class='sub-header'>Year-over-Year Comparison</h2>", unsafe_allow_html=True)
            
            # Group by year
            yearly_data = monthly_df.groupby('Year').agg({
                'Revenue': 'sum',
                'Profit': 'sum',
                'Transactions': 'sum'
            }).reset_index()
            
            # Calculate YoY changes
            yoy_data = []
            metrics = ['Revenue', 'Profit', 'Transactions']
            
            for metric in metrics:
                val_2023 = yearly_data[yearly_data['Year'] == '2023'][metric].values[0]
                val_2024 = yearly_data[yearly_data['Year'] == '2024'][metric].values[0]
                pct_change = ((val_2024 / val_2023) - 1) * 100
                
                yoy_data.append({
                    'Metric': metric,
                    '2023 Value': val_2023,
                    '2024 Value': val_2024,
                    'Change %': pct_change
                })
            
            yoy_df = pd.DataFrame(yoy_data)
            
            # Create YoY chart
            fig = go.Figure()
            
            for i, row in yoy_df.iterrows():
                metric = row['Metric']
                val_2023 = row['2023 Value']
                val_2024 = row['2024 Value']
                pct_change = row['Change %']
                
                if metric in ['Revenue', 'Profit']:
                    val_format = '${:,.0f}'
                else:
                    val_format = '{:,.0f}'
                
                fig.add_trace(go.Bar(
                    x=['2023', '2024'],
                    y=[val_2023, val_2024],
                    name=metric,
                    text=[val_format.format(val_2023), val_format.format(val_2024)],
                    textposition='auto',
                    marker_color=['#3498DB', '#2ECC71'] if pct_change >= 0 else ['#3498DB', '#E74C3C']
                ))
            
            fig.update_layout(
                title=f'Year-over-Year Comparison (2023 vs 2024)',
                barmode='group',
                xaxis_title='Year',
                yaxis_title='Value',
                legend_title='Metric'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display YoY table
col1, col2, col3 = st.columns(3)

for i, row in yoy_df.iterrows():
    metric = row['Metric']
    val_2023 = row['2023 Value']
    val_2024 = row['2024 Value']
    pct_change = row['Change %']
    
    if i == 0:
        container = col1
    elif i == 1:
        container = col2
    else:
        container = col3
        
    with container:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-label'>{metric}</div>", unsafe_allow_html=True)
        
        if metric in ['Revenue', 'Profit']:
            st.markdown(f"<div class='metric-value'>${val_2024:,.0f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; color: {'green' if pct_change >= 0 else 'red'};'>{pct_change:.1f}% vs 2023 (${val_2023:,.0f})</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='metric-value'>{val_2024:,.0f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; color: {'green' if pct_change >= 0 else 'red'};'>{pct_change:.1f}% vs 2023 ({val_2023:,.0f})</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
