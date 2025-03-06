import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_sales_pie_chart(df, value_col='Transaction Amount', names_col='Category'):
    """
    Create a pie chart for sales distribution
    
    Parameters:
    df (pandas.DataFrame): Input dataframe
    value_col (str): Column name for values
    names_col (str): Column name for segments
    
    Returns:
    plotly.graph_objects: Pie chart figure
    """
    fig = px.pie(
        df, 
        values=value_col, 
        names=names_col,
        title=f'{names_col} Distribution by {value_col}',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_bar_chart(df, x_col, y_col, title, color_col=None, orientation='v'):
    """
    Create a bar chart
    
    Parameters:
    df (pandas.DataFrame): Input dataframe
    x_col (str): Column name for x-axis
    y_col (str): Column name for y-axis
    title (str): Chart title
    color_col (str): Column name for color coding
    orientation (str): 'v' for vertical, 'h' for horizontal
    
    Returns:
    plotly.graph_objects: Bar chart figure
    """
    if orientation == 'h':
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title,
            orientation='h',
            color=color_col,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
    else:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title,
            color=color_col,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
    return fig

def create_line_chart(df, x_col, y_cols, title):
    """
    Create a line chart
    
    Parameters:
    df (pandas.DataFrame): Input dataframe
    x_col (str): Column name for x-axis
    y_cols (str or list): Column name(s) for y-axis
    title (str): Chart title
    
    Returns:
    plotly.graph_objects: Line chart figure
    """
    fig = px.line(
        df, 
        x=x_col, 
        y=y_cols,
        title=title,
        markers=True
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title='Value',
        legend_title='Metric'
    )
    return fig
