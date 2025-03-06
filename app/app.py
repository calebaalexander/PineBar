import streamlit as st
import pandas as pd
import numpy as np
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

# DATA PROCESSING FUNCTIONS
def generate_data(option):
    """
    Generate synthetic data for Pine Bar analytics
    
    Parameters:
    option (str): Data period option, one of "2023 Full Year", "2024 Full Year", or "2025 (up to March 5)"
    
    Returns:
    pandas.DataFrame: Generated data
    """
    # Categories and items
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
    
    # Set random seed based on option for consistent results
    if option == "2023 Full Year":
        np.random.seed(2023)
        n_samples = 150
        year = "2023"
    elif option == "2024 Full Year":
        np.random.seed(2024)
        n_samples = 180
        year = "2024"
    else:  # 2025 data
        np.random.seed(2025)
        n_samples = 70
        year = "2025"
    
    # Create empty dataframe
    data = []
    
    # Generate synthetic data for each category
    for category, items in categories.items():
        for item in items:
            # Only include some items to match the number of samples
            if np.random.random() > 0.3:
                # Generate realistic metrics
                total_amount = np.random.randint(500, 25000)
                total_quantity = np.random.randint(10, int(total_amount / 10) + 1)
                transaction_count = np.random.randint(5, min(500, total_quantity + 1))
                
                # Calculate other metrics based on total
                zero_priced = np.random.randint(0, int(total_quantity * 0.05) + 1)
                disc_amount = -np.random.randint(0, int(total_amount * 0.15) + 1) if np.random.random() > 0.3 else 0
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
                cost_factor = {
                    "BEER": 0.35 + np.random.random() * 0.1,      # 35-45%
                    "COCKTAILS": 0.25 + np.random.random() * 0.1, # 25-35%
                    "FOOD": 0.4 + np.random.random() * 0.15,      # 40-55%
                    "SPIRITS": 0.3 + np.random.random() * 0.1,    # 30-40%
                    "WINE": 0.45 + np.random.random() * 0.1,      # 45-55%
                    "N/A": 0.15 + np.random.random() * 0.1,       # 15-25%
                    "Merch": 0.5 + np.random.random() * 0.2,      # 50-70%
                }
                
                cost = total_amount * cost_factor[category]
                profit = transaction_amount - cost
                profit_margin = (profit / transaction_amount * 100) if transaction_amount > 0 else 0
                
                data.append({
                    "SKU": item, 
                    "Category": category, 
                    "Total Amount": total_amount, 
                    "Total Quantity": total_quantity, 
                    "Total Transaction Count": transaction_count,
                    "Zero Priced Count": zero_priced, 
                    "Discounted Amount": disc_amount, 
                    "Discounted Quantity": disc_quantity, 
                    "Discounted Transaction Count": disc_transactions,
                    "Offered Amount": offered_amount, 
                    "Offered Quantity": offered_quantity, 
                    "Offered Transaction Count": offered_transactions,
                    "Loss Amount": loss_amount, 
                    "Loss Quantity": loss_quantity, 
                    "Loss Transaction Count": loss_transactions,
                    "Returned Amount": returned_amount, 
                    "Returned Quantity": returned_quantity, 
                    "Returned Transaction Count": returned_transactions,
                    "Transaction Amount": transaction_amount, 
                    "Transaction Quantity": transaction_quantity, 
                    "Transaction Count": transaction_count,
                    "Cost": cost, 
                    "Profit": profit,
                    "Profit Margin": profit_margin,
                    "Year": year
                })
    
    df = pd.DataFrame(data)
    return df

# VISUALIZATION FUNCTIONS
def create_metrics_row(df):
    """
    Create a row of key metrics cards
    
    Parameters:
    df (pandas.DataFrame): The data to display metrics for
    """
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

def create_category_breakdown(df):
    """
    Create category breakdown visualizations
    
    Parameters:
    df (pandas.DataFrame): The data to visualize
    """
    st.markdown("<h2 class='sub-header'>Category Overview</h2>", unsafe_allow_html=True)
    
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

def create_category_performance(df):
    """
    Create detailed category performance analysis
    
    Parameters:
    df (pandas.DataFrame): The data to analyze
    """
    st.markdown("<h2 class='sub-header'>Category Performance Analysis</h2>", unsafe_allow_html=True)
    
    # Group by category
    category_performance = df.groupby('Category').agg({
        'Transaction Amount': 'sum',
        'Transaction Count': 'sum',
        'Transaction Quantity': 'sum',
        'Profit': 'sum',
        'Cost': 'sum',
        'SKU': 'nunique'
    }).reset_index()
    
    # Calculate derived metrics
    category_performance['Profit Margin'] = (category_performance['Profit'] / category_performance['Transaction Amount'] * 100).round(1)
    category_performance['Avg Order Value'] = (category_performance['Transaction Amount'] / category_performance['Transaction Count']).round(2)
    category_performance['Avg Items Per Order'] = (category_performance['Transaction Quantity'] / category_performance['Transaction Count']).round(2)
    category_performance['Revenue Per Item'] = (category_performance['Transaction Amount'] / category_performance['Transaction Quantity']).round(2)
    category_performance['Revenue Share'] = (category_performance['Transaction Amount'] / df['Transaction Amount'].sum() * 100).round(1)
    category_performance['Profit Share'] = (category_performance['Profit'] / df['Profit'].sum() * 100).round(1)
    
    # Sort by revenue
    category_performance = category_performance.sort_values('Transaction Amount', ascending=False)
    
    # Create comparison bar chart
    fig = px.bar(
        category_performance,
        x='Category',
        y=['Revenue Share', 'Profit Share'],
        title='Revenue vs Profit Share by Category',
        barmode='group',
        color_discrete_sequence=['#3498db', '#2ecc71']
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create scatter plot of margin vs volume
    fig2 = px.scatter(
        category_performance,
        x='Transaction Amount',
        y='Profit Margin',
        size='Transaction Count',
        color='Category',
        title='Revenue vs Margin by Category',
        labels={'Transaction Amount': 'Total Revenue ($)', 'Profit Margin': 'Profit Margin (%)'},
        text='Category'
    )
    fig2.update_traces(textposition='top center')
    
    # Create normalized metrics bar chart
    fig3 = px.bar(
        category_performance,
        x='Category',
        y=['Avg Order Value', 'Revenue Per Item'],
        title='Average Order Value & Revenue Per Item by Category',
        barmode='group',
        color_discrete_sequence=['#f39c12', '#9b59b6']
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:


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
    
    # Format the DataFrame for display
    st.markdown("<h3>Detailed Category Metrics</h3>", unsafe_allow_html=True)
    
    display_df = category_performance.copy()
    display_df['Revenue'] = display_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
    display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
    display_df['Margin'] = display_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
    display_df['Orders'] = display_df['Transaction Count'].apply(lambda x: f"{x:,.0f}")
    display_df['Items'] = display_df['Transaction Quantity'].apply(lambda x: f"{x:,.0f}")
    display_df['Products'] = display_df['SKU']
    display_df['Avg Order'] = display_df['Avg Order Value'].apply(lambda x: f"${x:.2f}")
    display_df['Rev/Item'] = display_df['Revenue Per Item'].apply(lambda x: f"${x:.2f}")
    display_df['Rev Share'] = display_df['Revenue Share'].apply(lambda x: f"{x:.1f}%")
    display_df['Profit Share'] = display_df['Profit Share'].apply(lambda x: f"{x:.1f}%")
    
    cols_to_display = ['Category', 'Revenue', 'Profit', 'Margin', 'Orders', 'Items', 
                      'Products', 'Avg Order', 'Rev/Item', 'Rev Share', 'Profit Share']
    
    st.dataframe(display_df[cols_to_display], use_container_width=True)

def create_product_performance(df, metric_sort):
    """
    Create product performance analysis and visualization
    
    Parameters:
    df (pandas.DataFrame): The data to analyze
    metric_sort (str): The metric to sort by
    """
    st.markdown("<h2 class='sub-header'>Product Performance</h2>", unsafe_allow_html=True)
    
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
    if metric == 'Profit Margin':
        fig = px.bar(
            df_sorted,
            x=metric,
            y='SKU',
            title=title,
            orientation='h',
            color=color_values,
            text=df_sorted[metric].apply(lambda x: f"{x:.1f}%"),
            color_continuous_scale='Viridis',
            hover_data=['Category', 'Transaction Amount', 'Profit']
        )
        fig.update_traces(textposition='outside')
    elif metric == 'Transaction Count':
        fig = px.bar(
            df_sorted,
            x=metric,
            y='SKU',
            title=title,
            orientation='h',
            color=color_values,
            text=df_sorted[metric],
            color_discrete_sequence=px.colors.qualitative.Bold,
            hover_data=['Category', 'Transaction Amount', 'Profit']
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
            color_discrete_sequence=px.colors.qualitative.Bold,
            hover_data=['Category', 'Transaction Count', 'Profit Margin']
        )
        fig.update_traces(textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the data table
    with st.expander("View Detailed Product Data"):
        # Format columns for display
        display_df = df_sorted.copy()
        display_df['Revenue'] = display_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
        display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:,.0f}")
        display_df['Margin'] = display_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
        display_df['Orders'] = display_df['Transaction Count']
        display_df['Avg Order Value'] = (display_df['Transaction Amount'] / display_df['Transaction Count']).apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df[['SKU', 'Category', 'Revenue', 'Profit', 'Margin', 'Orders', 'Avg Order Value']], use_container_width=True)
    
    # Additional product insights
    st.markdown("<h3>Product Insights</h3>", unsafe_allow_html=True)
    
    # Get top product within each category
    top_by_category = df.sort_values('Transaction Amount', ascending=False).groupby('Category').first().reset_index()
    
    # Format for display
    top_category_df = top_by_category.copy()
    top_category_df['Revenue'] = top_category_df['Transaction Amount'].apply(lambda x: f"${x:,.0f}")
    top_category_df['Profit'] = top_category_df['Profit'].apply(lambda x: f"${x:,.0f}")
    top_category_df['Margin'] = top_category_df['Profit Margin'].apply(lambda x: f"{x:.1f}%")
    
    with st.expander("Top Selling Product by Category"):
        st.dataframe(top_category_df[['Category', 'SKU', 'Revenue', 'Profit', 'Margin']], use_container_width=True)

def create_profitability_analysis(df):
    """
    Create profitability analysis and visualizations
    
    Parameters:
    df (pandas.DataFrame): The data to analyze
    """
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
    
    # Define high and low margin thresholds
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
