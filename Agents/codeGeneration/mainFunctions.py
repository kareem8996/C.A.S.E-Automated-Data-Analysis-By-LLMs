import plotly.express as px
import pandas as pd
import numpy as np
from loggerModule import setup_logging
logger=setup_logging()

data=px.data.iris() # temp variable until we read from db

def create_pairplot(color=None, dimensions=None, diagonal_visible=True,title='Pair Plot'):
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
        df = px.data.iris()
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


def create_radar_chart( category_column, value_columns=None, title="Radar Chart", color_column=None):
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
    data = pd.DataFrame({
        "Category": ["A", "B", "C"],
        "Metric 1": [10, 20, 30],
        "Metric 2": [40, 50, 60],
        "Metric 3": [70, 80, 90],
        "Group": ["X", "Y", "X"]
    })
    try:
        if category_column not in data.columns:
            raise ValueError(f"Category column '{category_column}' is not in the DataFrame.")

        
        # Default value columns to all numeric columns except the category column
        if value_columns is None:
            value_columns = data.select_dtypes(include=['number']).columns.difference([category_column]).tolist()
        
        if not value_columns:
            raise ValueError("No numerical columns found for plotting.")
        
        # Check if the color column exists
        if color_column and color_column not in data.columns:
            raise ValueError(f"Color column '{color_column}' is not in the DataFrame.")
        
        # Melt the data for radar chart format
        melted_data = data.melt(
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



def create_treemap(path_columns, value_column=None, color_column=None, title="Treemap", color_scale="Viridis"):
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

        valid_path_columns = [col for col in path_columns if col in data.columns]
        if len(valid_path_columns) < len(path_columns):
            missing_cols = set(path_columns) - set(valid_path_columns)
            print(f"Warning: The following columns are missing and will be removed: {missing_cols}")

        # Ensure there is at least one valid path column
        if not valid_path_columns:
            print("Warning: No valid columns for the treemap hierarchy. Returning None.")
            return None
        
        # Check value and color columns
        if value_column and value_column not in data.columns:
            print(f"Warning: Value column '{value_column}' is not in the DataFrame. Ignoring it.")
            value_column = None
        
        if color_column and color_column not in data.columns:
            print(f"Warning: Color column '{color_column}' is not in the DataFrame. Ignoring it.")
            color_column = None
        
        # Handle missing values in relevant columns
        all_columns = valid_path_columns + [value_column, color_column]
        for col in filter(None, all_columns):  # Skip None columns
            if col in data.columns:
                data[col] = data[col].fillna(None)
        

        data["all"] = "all" # in order to have a single root node

        # Create the treemap
        fig = px.treemap(
            data,
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




def create_correlation_heatmap(columns=None, color_scale="Viridis", title="Correlation Heatmap", show_values=True):
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
        # Filter for numerical columns
        numerical_data = data.select_dtypes(include=["number"])

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
