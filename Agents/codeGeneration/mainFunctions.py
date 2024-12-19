import plotly.express as px
import pandas as pd
import numpy as np
from loggerModule import setup_logging
logger=setup_logging()

def create_pairplot(color=None, dimensions=None, diagonal_visible=True):
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
            fig = px.scatter_matrix(df, color=color,symbol=color, dimensions=dimensions)
        else:
            fig = px.scatter_matrix(df, color=color,symbol=color)

        fig.update_traces(diagonal_visible=diagonal_visible)
        logger.info(f"Pair Plot Created Successfully")
        return fig
    except ValueError as e:
        logger.error(f"ValueError: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")