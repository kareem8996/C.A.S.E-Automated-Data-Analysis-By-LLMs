import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter
from Agents.codeGeneration import mainFunctions
import json
import numpy as np
import time
viz_router = APIRouter()

def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.float64, float)) and (np.isnan(obj) or np.isinf(obj)):
        return None
    else:
        return obj


@viz_router.get('/visualization/{project_id}')
async def visualization(project_id:str):
    """
    Endpoint to retrieve visualization data for a project.

    Args:
        project_id (str): Project ID to retrieve visualization data for.

    Returns:
        dict: JSON with visualization data.
    """
    fig2 = mainFunctions.scatter_plot(x='Fare', y='Age',project_id=project_id)
    fig2 = make_serializable(fig2.to_dict())
    
    # Visualization 3
    fig3 = mainFunctions.line_plot(x='Fare', y='Age',project_id=project_id)
    fig3 = make_serializable(fig3.to_dict())
    # time.sleep(10)
    return {'visualizations':[fig2, fig3]}
