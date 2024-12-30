import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import requests


def fetch_visualizations(project_id):
    url = f'http://127.0.0.1:8000/visualization/{project_id}'
    response = requests.get(url)
    return response.json()['visualizations']