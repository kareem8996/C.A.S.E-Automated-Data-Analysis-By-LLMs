import pandas as pd
from typing import Dict
import google.generativeai as genai

class AgentGraphState(Dict):

    pass

def data_description_generator_node(state: AgentGraphState, model, temperature=0) -> AgentGraphState:
    """
    A node in the graph that generates a description of the dataset, its schema, and basic statistics.

    Args:
        model: The generative AI model (e.g., Gemini).
        temperature: Controls the randomness of the model's output.

    Returns:
        The updated state with the description, schema, and basic statistics.
    """
    # Check if the dataset is provided in the state
    if "df" not in state:
        raise ValueError("No dataset provided in state.")

    df = state["df"]

    schema = df.columns.tolist()

    basic_stats = df.describe(include='all').reset_index()

    prompt = f"""
    Given the dataset:
    {df.head()}

    Provide the following:
    1. A detailed explanation of each column in bullet points.
    2. An overview description of the dataset.
    """

    response = model.generate_content(prompt)

    state["description"] = response.text
    state["schema"] = schema
    state["basic_stats"] = basic_stats

    return state
    #The updated state with the description, schema, and basic statistics.