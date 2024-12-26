import streamlit as st
import pandas as pd
import os

# Directory to store datasets
DATASET_DIR = "datasets"

# Ensure the directory exists
os.makedirs(DATASET_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the dataset directory."""
    file_path = os.path.join(DATASET_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_existing_datasets():
    """Load the list of existing datasets."""
    return [f for f in os.listdir(DATASET_DIR) if f.endswith((".csv", ".xlsx"))]

def load_dataset(file_name):
    """Load a dataset by file name."""
    file_path = os.path.join(DATASET_DIR, file_name)
    if file_name.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_path)

# Streamlit App
st.title("Multi-Dataset Manager")

# Page Navigation
page = st.sidebar.radio("Navigation", ["View Datasets", "Add New Dataset"])

if page == "View Datasets":
    st.header("Your Datasets")

    # Load existing datasets
    datasets = load_existing_datasets()
    
    if datasets:
        selected_file = st.selectbox("Select a dataset to view", datasets)
        
        if selected_file:
            # Display dataset
            st.subheader(f"Viewing Dataset: {selected_file}")
            try:
                df = load_dataset(selected_file)
                st.write(df)
                st.write("Summary Statistics:")
                st.write(df.describe())
            except Exception as e:
                st.error(f"Error loading dataset: {e}")
            
            # Option to delete dataset
            if st.button(f"Delete {selected_file}"):
                os.remove(os.path.join(DATASET_DIR, selected_file))
                st.success(f"{selected_file} has been deleted.")
                st.experimental_rerun()
    else:
        st.info("No datasets available. Add a new one in the 'Add New Dataset' tab.")

elif page == "Add New Dataset":
    st.header("Add New Dataset")

    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        # Save the uploaded file
        try:
            save_uploaded_file(uploaded_file)
            st.success(f"{uploaded_file.name} has been uploaded successfully!")
        except Exception as e:
            st.error(f"Error saving file: {e}")
