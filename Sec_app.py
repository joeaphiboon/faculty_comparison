import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from dotenv import load_dotenv
import base64
from io import StringIO

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Faculty Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Prevent data download
st.markdown("""
    <style>
        .downloadButton {
            display: none !important;
        }
        .stDownloadButton {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# [Your SKILL_GROUPS dictionary remains the same]
SKILL_GROUPS = {
    'Core Skills': [
        'avg Self-Awareness',
        'avg Confidence',
        'avg Positive Attitude',
        'avg Communication',
        'avg Creativity',
        'avg Global Competence'
    ],
    'PISA Communication': [
        'avg Communication',
        'Encode',
        'Decode',
        'Plan',
        'Communicationandcollaboration'
    ],
    'PISA Leadership': [
        'Leadershipandprojectmanagement',
        'Criticalthinkingandproblemsolving',
        'Criticalthinking',
        'Self-confidence',
        'Initiative',
        'Showdedication',
        'Responsibilitytaking'
    ],
    'PISA Global Competence': [
        'avg Global Competence',
        'Globalcitizen',
        'Interculturalawareness',
        'Open-minded',
        'Explorationandopennesstonewperspectives',
        'Collaborationandcollectivecreativity',
        'Emotions',
        'Personalgrowth',
        'Self-reflection'
    ]
}

def format_metric_name(name):
    """Format metric names for better readability."""
    name = name.replace('avg ', '')
    name = ''.join([' ' + c if c.isupper() else c for c in name]).strip()
    name = name.replace(' and ', ' & ')
    return name.title()

@st.cache_data
def load_data():
    """Load and preprocess the data securely."""
    try:
        # First try to load from Streamlit secrets (for cloud deployment)
        if 'csv_data' in st.secrets:
            encoded_data = st.secrets["csv_data"]
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            df = pd.read_csv(StringIO(decoded_data))
        else:
            # Fall back to local file (for development)
            data_path = os.getenv('DATA_PATH', 'data/Faculty_Comparison_of_Z-Scores.csv')
            df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error("Error loading data. Please check data configuration.")
        return None

# [Rest of your functions remain the same: create_radar_chart, create_bar_chart, create_line_chart]

# Main app
def main():
    st.title("Faculty Performance Analysis Dashboard")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Unable to load data. Please contact the administrator.")
        return
        
    # [Rest of your main() function remains the same]

if __name__ == "__main__":
    main()