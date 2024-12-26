import plotly.express as px
import pandas as pd
import seaborn as sns

# Loading sample datasets 
iris = sns.load_dataset('iris')
Tips = px.data.tips()


def line_plot(x, y, color=None, labels=None, title=None,width=800, height=600):
    """
    Generates a line plot using Plotly Express.

    Parameters:
    - data_frame (DataFrame): The dataframe containing the data to be plotted.
    - x (str): The column name to be used for the x-axis.
    - y (str): The column name to be used for the y-axis.
    - color (str, optional): Column name to set the line color, useful for grouping.
    - labels (dict, optional): A dictionary of axis label mappings for x and y.
    - title (str, optional): The title of the plot.

    Returns:
    - fig (Figure): A Plotly Figure object that can be displayed.
    """
    try:
        data = iris
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in iris.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
        
        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.line(
            data_frame=iris,
            x=x,
            y=y,
            color=color,
            symbol=color,
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.set1,
            title=title,
            template="plotly_dark",
            width=width,
            height=height
        )
        return fig
    except Exception as e:
        print(f"Error creating line plot: {e}")


def scatter_plot(x, y, color=None, labels=None, 
                marginal_x=None, marginal_y=None, trendline=None, 
                trendline_scope=None, title=None, 
                width=800, height=600):
    """
    Generates a scatter plot using Plotly Express.

    Parameters:
    - data_frame (DataFrame): The dataframe containing the data to be plotted.
    - x (str): The column name for the x-axis.
    - y (str): The column name for the y-axis.
    - color (str, optional): Column name to differentiate points by color (e.g., groups or categories).
    - symbol (str, optional): Column name to differentiate points by symbols.
    - labels (dict, optional): Dictionary of axis label mappings for x and y.
    - trendline (str, optional): Type of trendline to draw (e.g., 'ols', 'lowess').
    - trendline_scope (str, optional): Whether trendlines are fit per trace or across traces (default: 'trace').
    - title (str, optional): The title of the plot.
    - width (int, optional): Width of the plot in pixels (default: 800).
    - height (int, optional): Height of the plot in pixels (default: 600).

    Returns:
    - fig (Figure): A Plotly Figure object that can be displayed.
    """
    try:
        data = iris
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in iris.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
                
        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns 
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.scatter(
            data_frame=iris,
            x=x,
            y=y,
            color=color,
            symbol=color,
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.set1,
            marginal_x=marginal_x,
            marginal_y=marginal_y,
            trendline=trendline,
            trendline_scope=trendline_scope,
            title=title,
            template='plotly_dark',
            width=width,
            height=height
        )
        return fig
    except Exception as e:
        print(f"Error creating scatter plot: {e}")


def bubble_plot(x, y, color=None, size=None, labels=None, 
                title=None, width=800, height=600): 
    """
    Generates a bubble plot using Plotly Express.

    Parameters:
    - data_frame (DataFrame): The dataframe containing the data to be plotted.
    - x (str): The column name for the x-axis.
    - y (str): The column name for the y-axis.
    - color (str, optional): Column name to differentiate points by color (e.g., groups or categories).
    - symbol (str, optional): Column name to differentiate points by symbols.
    - size (str, optional): Column name representing the size of the bubbles.
    - labels (dict, optional): Dictionary of axis label mappings for x and y.
    - color_discrete_sequence (list, optional): List of colors for categorical data.
    - title (str, optional): The title of the plot.
    - template (str, optional): Plotly template (default: 'plotly').
    - width (int, optional): Width of the plot in pixels (default: 800).
    - height (int, optional): Height of the plot in pixels (default: 600).

    Returns:
    - fig (Figure): A Plotly Figure object that can be displayed.
    """
    try:
        data = iris
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in iris.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
            
        #converting passed parameter size into integer
        if size.astype(str).str.contains('float').any():
            size = size.astype(int) 

        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.scatter(
            data_frame=iris,
            x=x,
            y=y,
            color=color,
            symbol=color,
            size=size,
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.set1,
            title=title,
            template="plotly_dark",
            width=width,
            height=height
        )
        return fig
    except Exception as e:
        print(f"Error creating bubble plot: {e}")


def swarm_plot(x,y,color=None,labels=None,stripmode="group",title=None,width=800,height=600):
    """
    Creates a swarm plot (approximated using scatter plot) using Plotly Express.

    Parameters:
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        color (str, optional): Column name to group points by color.
        labels (dict, optional): Dictionary of axis or legend labels.
        stripmode (str, optional): Mode for strip plot, e.g., "group".
        title (str, optional): Title of the plot.
        width (int, optional): Width of the plot in pixels (default is 800).
        height (int, optional): Height of the plot in pixels (default is 600).

    Returns:
        fig: A Plotly figure object.
    """
    try:
        data = Tips
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in iris.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
        
        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.strip(
            data_frame=Tips,
            x=x, 
            y=y, 
            color=color,
            symbol = color, 
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.Set1, 
            orientation="v", 
            stripmode=stripmode, 
            title=title, 
            template="plotly_dark", 
            width=width, 
            height=height 
)
        return fig
    except Exception as e:
        print(f"Error creating swarm plot: {e}")


def grouped_bar_plot(x, y, color=None, title="Grouped Bar Plot"):
    """
    Creates a grouped bar plot using Plotly Express.

    Parameters:
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        color (str, optional): Column name to group bars by color.
        title (str, optional): Title of the plot (default is "Grouped Bar Plot").

    Returns:
        fig: A Plotly figure object.
    """
    try:
        data = Tips
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in iris.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")

        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.bar(
            Tips, 
            x=x, 
            y=y, 
            color=color, 
            title=title, 
            barmode="group"
            )
        return fig
    except Exception as e:
        print(f"Error creating grouped bar plot: {e}")
