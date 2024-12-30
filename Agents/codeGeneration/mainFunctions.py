import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
from . import loggerModule
import sys
import os
import pandas as pd
from io import StringIO

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database import mainDatabase

logger=loggerModule.setup_logging()

def line_plot(x, y, color=None, labels=None, title=None,width=800, height=600,project_id=None):
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
        df=mainDatabase.fetch_dataset(project_id)
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in df.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
        
        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        df = df.dropna(subset=relevant_columns)

        fig = px.line(
            data_frame=df,
            x=x,
            y=y,
            color=color,
            symbol=color,
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.Set1,
            title=title,
            template="plotly_dark",
        )
        return fig
    except Exception as e:
        print(f"Error creating line plot: {e}")


def scatter_plot(x, y, color=None, labels=None, 
                marginal_x=None, marginal_y=None, trendline=None, 
                trendline_scope=None, title=None,project_id=None):
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
        data=mainDatabase.fetch_dataset(project_id)
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in data.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
                
        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns 
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.scatter(
            data_frame=data,
            x=x,
            y=y,
            color=color,
            symbol=color,
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.Set1,
            marginal_x=marginal_x,
            marginal_y=marginal_y,
            trendline=trendline,
            trendline_scope=trendline_scope,
            title=title,
            template='plotly_dark',
        )
        return fig
    except Exception as e:
        print(f"Error creating scatter plot: {e}")


def bubble_plot(x, y, color=None, size=None, labels=None, 
                title=None, width=800, height=600,project_id=None): 
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
        df=mainDatabase.fetch_dataset(project_id)

        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in df.columns:
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
            data_frame=df,
            x=x,
            y=y,
            color=color,
            symbol=color,
            size=size,
            labels=labels,
            color_discrete_sequence=px.colors.qualitative.Set1,
            title=title,
            template="plotly_dark",
        )
        return fig
    except Exception as e:
        print(f"Error creating bubble plot: {e}")


def swarm_plot(x,y,color=None,labels=None,stripmode="group",title=None,project_id=None):
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
        df=mainDatabase.fetch_dataset(project_id)
        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in df.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")
        
        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.strip(
            data_frame=df,
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
)
        return fig
    except Exception as e:
        print(f"Error creating swarm plot: {e}")


def grouped_bar_plot(x, y, color=None, title="Grouped Bar Plot",project_id=None):
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
        df=mainDatabase.fetch_dataset(project_id)

        # Check if provided column names exist in the dataset
        for col in [x, y, color]:
            if col and col not in df.columns:
                raise ValueError(f"The specified '{col}' column is not found in the dataset.")

        # check if the specified columns are the same
        if x == y or x == color or y == color:
            raise ValueError("The specified x, y, or color column is the same as the other column.")
        
        # drop rows with missing values in the relevant columns
        relevant_columns = [col for col in [x, y, color] if col is not None]
        data = data.dropna(subset=relevant_columns)

        fig = px.bar(
            df, 
            x=x, 
            y=y, 
            color=color, 
            title=title, 
            barmode="group"
            )
        return fig
    except Exception as e:
        print(f"Error creating grouped bar plot: {e}")

def create_pairplot(color=None, dimensions=None, diagonal_visible=True,title='Pair Plot',project_id=None):
    """
    Create a pairplot using Plotly.

    Parameters:
    color (str): Column name to be used for color encoding.
    dimensions (list): List of column names to be used as dimensions for the pairplot.
    diagonal_visible (bool): Whether to show the diagonal plots.

    Returns:
    fig: Plotly figure object representing the pairplot.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Check if DataFrame has more than one column
        if df.shape[1] < 2:
            raise ValueError("DataFrame must have at least two columns for a pairplot.")
        
        # Create the pairplot using Plotly
        if dimensions is not None:
            fig = px.scatter_matrix(df, color=color,symbol=color, dimensions=dimensions,title=title)
        else:
            fig = px.scatter_matrix(df, color=color,symbol=color,title=title)

        fig.update_traces(diagonal_visible=diagonal_visible)
        logger.info(f"Pair Plot Created Successfully")
        fig.update_layout(
                template="plotly_dark",)
        return fig
        
    except ValueError as e:
        logger.error(f"ValueError: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def create_radar_chart( category_column, value_columns=None, title="Radar Chart", color_column=None,project_id=None):
    """
    Generates a radar chart using Plotly Express.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        category_column (str): The column name that defines the categories (radial axis).
        value_columns (list, optional): List of column names to plot as radar lines.
                                         If None, all numerical columns except the category column will be used.
        title (str, optional): The title of the radar chart. Default is "Radar Chart".
        color_column (str, optional): Column name for grouping different lines (optional).
                                       If None, no grouping is applied.

    Returns:
        plotly.graph_objects.Figure: The generated radar chart.
    """
    # Example dataset
    df=mainDatabase.fetch_dataset(project_id)

    try:
        if category_column not in df.columns:
            raise ValueError(f"Category column '{category_column}' is not in the DataFrame.")

        
        # Default value columns to all numeric columns except the category column
        if value_columns is None:
            value_columns = df.select_dtypes(include=['number']).columns.difference([category_column]).tolist()
        
        if not value_columns:
            raise ValueError("No numerical columns found for plotting.")
        
        # Check if the color column exists
        if color_column and color_column not in df.columns:
            raise ValueError(f"Color column '{color_column}' is not in the DataFrame.")
        
        # Melt the data for radar chart format
        melted_data = df.melt(
            id_vars=[category_column] + ([color_column] if color_column else []),
            value_vars=value_columns,
            var_name="Metric",
            value_name="Value"
        )
        
        # Create the radar chart
        fig = px.line_polar(
            melted_data,
            r="Value",
            theta="Metric",
            color=color_column,
            line_close=True,
            title=title,
        )
        fig.update_traces(fill="toself")
        logger.info(f"Radar Plot Created Successfully")

        fig.update_layout(
                template="plotly_dark",)
        return fig  

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None



def create_treemap(path_columns, value_column=None, color_column=None, title="Treemap", color_scale="Viridis",project_id=None):
    """
    Generates a treemap using Plotly Express.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        path_columns (list): A list of columns defining the hierarchy for the treemap.
        value_column (str, optional): The column to determine the size of the segments. If None, all segments will be of equal size.
        color_column (str, optional): The column to determine the color of the segments. If None, no color mapping is applied.
        title (str, optional): Title of the treemap. Default is "Treemap".
        color_scale (str, optional): Color scale to use for the treemap. Default is "Viridis".

    Returns:
        plotly.graph_objects.Figure: The generated treemap.
    """
    try:  
        df=mainDatabase.fetch_dataset(project_id)

        valid_path_columns = [col for col in path_columns if col in df.columns]
        if len(valid_path_columns) < len(path_columns):
            missing_cols = set(path_columns) - set(valid_path_columns)
            print(f"Warning: The following columns are missing and will be removed: {missing_cols}")

        # Ensure there is at least one valid path column
        if not valid_path_columns:
            print("Warning: No valid columns for the treemap hierarchy. Returning None.")
            return None
        
        # Check value and color columns
        if value_column and value_column not in df.columns:
            print(f"Warning: Value column '{value_column}' is not in the DataFrame. Ignoring it.")
            value_column = None
        
        if color_column and color_column not in df.columns:
            print(f"Warning: Color column '{color_column}' is not in the DataFrame. Ignoring it.")
            color_column = None
        
        # Handle missing values in relevant columns
        all_columns = valid_path_columns + [value_column, color_column]
        for col in filter(None, all_columns):  # Skip None columns
            if col in df.columns:
                df[col] = df[col].fillna(None)
        

        df["all"] = "all" # in order to have a single root node

        # Create the treemap
        fig = px.treemap(
            df,
            path=valid_path_columns,
            values=value_column,
            color=color_column,
            title=title,
            color_continuous_scale=color_scale
        )
        fig.update_traces(root_color="lightgrey")
        fig.update_traces(marker=dict(cornerradius=5))

        logger.info(f"Tree Map Plot Created Successfully")

        fig.update_layout(
                template="plotly_dark",)
        return fig

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None




def create_correlation_heatmap(columns=None, color_scale="Viridis", title="Correlation Heatmap", show_values=True,project_id=None):
    """
    Generates a heatmap of correlations between numerical columns in the dataset.

    Args:
        data (pd.DataFrame): The input dataset. Must be a pandas DataFrame.
        columns (list, optional): List of specific columns to include in the correlation. Default is None (use all numerical columns).
        color_scale (str, optional): Color scale to use for the heatmap. Default is "Viridis".
        title (str, optional): Title of the heatmap. Default is "Correlation Heatmap".
        show_values (bool, optional): Whether to overlay correlation values on the heatmap. Default is True.

    Returns:
        plotly.graph_objects.Figure: The generated correlation heatmap.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Filter for numerical columns
        numerical_data = df.select_dtypes(include=["number"])

        # Use specified columns if provided
        if columns:
            numerical_data = numerical_data[columns]

        # Calculate correlation matrix
        correlation_matrix = numerical_data.corr()

        # Replace NaN values with None for compatibility with Plotly
        correlation_matrix = correlation_matrix.applymap(lambda x: None if pd.isna(x) else x)

        # Create heatmap
        fig = px.imshow(
            correlation_matrix,
            labels=dict(x="Features", y="Features", color="Correlation"),
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            color_continuous_scale=color_scale,
            title=title
        )

        # Optionally add correlation values as text
        if show_values:
            fig.update_traces(text=correlation_matrix.values, texttemplate="%{text:.2f}", textfont_size=12)
        
        logger.info(f"Heatmap Created Successfully")
        fig.update_layout(
                template="plotly_dark",)
        return fig

    except KeyError as e:
        logger.error(f"Error: Some specified columns are not in the dataset. Details: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


def create_faceted_bar_chart(
    x,
    y,
    color=None,
    barmode="group",
    facet_row=None,
    facet_col=None,
    title="Faceted Bar Chart",
    project_id=None
):
    """
    Generates a faceted bar chart using Plotly Express with null value handling.

    Args:
        data (pd.DataFrame): Input dataset as a pandas DataFrame.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        color (str, optional): Column name for bar colors. Default is None.
        barmode (str, optional): Bar mode. Options: 'group', 'overlay', 'relative'. Default is 'group'.
        facet_row (str, optional): Column name for facet rows. Default is None.
        facet_col (str, optional): Column name for facet columns. Default is None.
        category_orders (dict, optional): Custom ordering for categorical columns. Default is None.
        title (str, optional): Title of the chart. Default is "Faceted Bar Chart".
        color_scale (str, optional): Color scale for the bars. Default is "Viridis".
        null_handling (str, optional): How to handle null values: "drop", "fill", or "ignore". Default is "drop".
        fill_value (str/int/float, optional): Value to replace nulls if null_handling="fill". Default is "Unknown".

    Returns:
        plotly.graph_objects.Figure: The generated faceted bar chart.
    """
    try:
        # Null handling
        # Drop rows with nulls in relevant columns
        df=mainDatabase.fetch_dataset(project_id)

        relevant_columns = [col for col in [x, y, color, facet_row, facet_col] if col]
        df = df.dropna(subset=relevant_columns)

        # Ensure specified columns exist
        required_columns = [x, y, color, facet_row, facet_col]
        for col in required_columns:
            if col and col not in df.columns:
                print(f"Warning: Column '{col}' not found in data. Ignoring it.")
                if col == x or col == y:
                    raise ValueError(f"Essential column '{col}' is missing. Cannot create chart.")

        # Create the faceted bar chart
        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            barmode=barmode,
            facet_row=facet_row,
            facet_col=facet_col,
            title=title,
            
        )

        # Update layout for better aesthetics
        fig.update_layout(
            title=dict(x=0.5),  # Center the title
            coloraxis_colorbar=dict(title=color),  # Label the color axis if color is used
            font=dict(size=12),
        )
        fig.update_layout(
                template="plotly_dark",)
        logger.info(f"Facet Bar Chart Created Successfully")

        return fig

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None
    
def create_histogram(x, color=None, x_label=None, y_label=None,project_id=None):
    """
    Create a histogram using Plotly Express.
    
    Parameters:
        data (DataFrame): The dataset to plot.
        x (str): The column name for the x-axis.
        color (str, optional): The column name to be used for color encoding. Default is None.
        x_label (str, optional): Label for the x-axis. Default is None.
        y_label (str, optional): Label for the y-axis. Default is None.
    
    Returns:
        fig (plotly.graph_objs._figure.Figure): The histogram figure object.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Check if the x column exists in the data
        if x not in df.columns:
            raise ValueError(f"Column '{x}' not found in the dataset.")

        # Create the histogram
        fig = px.histogram(df, x=x, color=color) 
        return fig
    except Exception as e:
        #logger.error(f"An error occurred while creating the histogram: {e}")
        print(f"An error occurred while creating the histogram: {e}")
        
        
        
def create_pie_chart(values, names, color=None, title=None,project_id=None):
    """
    Create a pie chart using Plotly Express.

    Parameters:
        data (DataFrame): The dataset to plot.
        values (str): The column name for the values.
        names (str): The column name for the names (labels).
        color (str, optional): The column name to be used for color encoding. Default is None.
        title (str, optional): The title of the pie chart. Default is None.

    Returns:
        fig (plotly.graph_objs._figure.Figure): The pie chart figure object.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Check if the values and names columns exist in the data
        if values not in df.columns:
            raise ValueError(f"Column '{values}' not found in the dataset.")
        if names not in df.columns:
            raise ValueError(f"Column '{names}' not found in the dataset.")

        # Create the pie chart
        fig = px.pie(df, values=values, names=names, color=color, title=title)
        return fig
    except Exception as e:
        print(f"An error occurred while creating the pie chart: {e}")
        
        
        
def create_area_chart(x, y, color=None, x_label=None, y_label=None, title=None,project_id=None):
    """
    Create an area chart using Plotly Express.

    Parameters:
        data (DataFrame): The dataset to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        color (str, optional): The column name to be used for color encoding. Default is None.
        x_label (str, optional): Label for the x-axis. Default is None.
        y_label (str, optional): Label for the y-axis. Default is None.
        title (str, optional): Title of the area chart. Default is None.

    Returns:
        fig (plotly.graph_objs._figure.Figure): The area chart figure object.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Check if the x and y columns exist in the data
        if x not in df.columns:
            raise ValueError(f"Column '{x}' not found in the dataset.")
        if y not in df.columns:
            raise ValueError(f"Column '{y}' not found in the dataset.")

        # Create the area chart
        fig = px.area(df, x=x, y=y, color=color, title=title, labels={'x': x_label, 'y': y_label})
        return fig
    except Exception as e:
        print(f"Error creating area chart: {e}")
        
        
def create_boxplot(x=None, y=None, color=None, x_label=None, y_label=None,project_id=None):
    """
    Create a box plot using Plotly Express.
    
    Parameters:
        data (DataFrame): The dataset to plot.
        x (str, optional): The column name for the x-axis. Default is None.
        y (str): The column name for the y-axis.
        color (str, optional): The column name to be used for color encoding. Default is None.
        x_label (str, optional): Label for the x-axis. Default is None.
        y_label (str, optional): Label for the y-axis. Default is None.
    
    Returns:
        fig (plotly.graph_objs._figure.Figure): The box plot figure object.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Check if y column exists in the data
        if y not in df.columns:
            raise ValueError(f"Column '{y}' not found in the dataset.")
        
        # Check if x column exists (if provided)
        if x and x not in df.columns:
            raise ValueError(f"Column '{x}' not found in the dataset.")
        
        # Check if color column exists (if provided)
        if color and color not in df.columns:
            raise ValueError(f"Column '{color}' not found in the dataset.")

        # Create the box plot
        fig = px.box(df, x=x, y=y, color=color)
        
        # Update axis labels if provided
        if x_label:
            fig.update_xaxes(title_text=x_label)
        if y_label:
            fig.update_yaxes(title_text=y_label)
        return fig
    except Exception as e:
        print(f"Error: {e}")
        
        
def create_violin_plot(x=None, y=None, color=None, points=None, hover_data=None, x_label=None, y_label=None,project_id=None):
    """
    Create a violin plot using Plotly Express.
    
    Parameters:
        data (DataFrame): The dataset to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        color (str, optional): The column name to be used for color encoding. Default is None.
        points (str, optional): Whether to show data points. Options are 'all', 'outliers', 'suspectedoutliers', or 'false'. Default is 'all'.
        hover_data (list, optional): Additional data to display when hovering over points. Default is None.
        x_label (str, optional): Label for the x-axis. Default is None.
        y_label (str, optional): Label for the y-axis. Default is None.
    
    Returns:
        fig (plotly.graph_objs._figure.Figure): The violin plot figure object.
    """
    try:
        df=mainDatabase.fetch_dataset(project_id)

        # Check if y column exists in the data
        if y not in df.columns:
            raise ValueError(f"Column '{y}' not found in the dataset.")
        
        # Check if x column exists (if provided)
        if x and x not in df.columns:
            raise ValueError(f"Column '{x}' not found in the dataset.")
        
        # Check if color column exists (if provided)
        if color and color not in df.columns:
            raise ValueError(f"Column '{color}' not found in the dataset.")

        # Create the violin plot
        fig = px.violin(df, x=x, y=y, color=color, points=points, hover_data=hover_data)
        
        # Update axis labels if provided
        if x_label:
            fig.update_xaxes(title_text=x_label)
        if y_label:
            fig.update_yaxes(title_text=y_label)
        return fig
    except Exception as e:
       print(f"An error occurred: {e}")  
