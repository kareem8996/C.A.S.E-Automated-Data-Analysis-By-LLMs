import streamlit as st

# Define projects
projects = [
    {"name": "demo2", "date": "26 Dec 2024", "models": 0, "color": "#6A0DAD"},
    {"name": "demk", "date": "26 Dec 2024", "models": 0, "color": "#FF0000"},
    {"name": "project3", "date": "27 Dec 2024", "models": 1, "color": "#1E90FF"},
    {"name": "project4", "date": "28 Dec 2024", "models": 3, "color": "#32CD32"},
    {"name": "project5", "date": "29 Dec 2024", "models": 2, "color": "#FFD700"},
]

st.title("My Workspaces")

# Limit columns to 3 per row
max_columns = 3
columns = None

for idx, project in enumerate(projects):
    if idx % max_columns == 0:  # Create a new row every 3 projects
        columns = st.columns(max_columns)
    
    with columns[idx % max_columns]:  # Add project to the appropriate column
        st.markdown(
    f"""
    <style>
    .custom-button {{
        border-radius: 16px;
        background: rgba(0, 0, 0, 0.4);
        z-index: 2;
        box-shadow: 
            0 0 6px rgba(255, 255, 255, 0.3), 
            0 0 12px rgba(255, 255, 255, 0.2), 
            0 0 18px {project['color']}44;
        color: white;
        padding: 30px;
        font-size: 16px;
        text-align: center;
        cursor: pointer;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px; /* Adds vertical space if wrapping occurs */

        transition: box-shadow 0.3s ease; /* Smooth transition */
    }}
    .custom-button:hover {{
        box-shadow: 
            0 0 10px rgba(255, 255, 255, 0.6), 
            0 0 20px rgba(255, 255, 255, 0.5), 
            0 0 30px {project['color']}88; /* Stronger glow on hover */
    }}
    </style>
    <div class="custom-button" onclick="window.location.href='#';">
        <h3>{project['name']}</h3>
        <p>{project['date']}</p>    
    </div>
    """,
    unsafe_allow_html=True,
)



# Add a button to create a new workspace
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <button style="
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        " onclick="window.location.href='#';">+ Create a new workspace</button>
    </div>
    """,
    unsafe_allow_html=True,
)
