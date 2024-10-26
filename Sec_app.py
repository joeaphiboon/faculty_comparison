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

def create_radar_chart(df, selected_faculty, skill_group='Core Skills'):
    """Create a radar chart for the selected faculty."""
    categories = SKILL_GROUPS[skill_group]
    formatted_categories = [format_metric_name(cat) for cat in categories]  # Pre-format categories
    values = df[df['Faculty'] == selected_faculty][categories].values.flatten().tolist()
    
    # Add the first value and category at the end to close the polygon
    formatted_categories_closed = formatted_categories + [formatted_categories[0]]
    values_closed = values + [values[0]]
    
    # Calculate global min and max for selected metrics across all faculties
    metrics_data = df[categories]
    global_min = metrics_data.min().min()
    global_max = metrics_data.max().max()
    
    fig = go.Figure()
    
    # Add zero line trace with fixed category sequence
    fig.add_trace(go.Scatterpolar(
        r=[0] * (len(categories) + 1),  # Add extra point to close the zero line
        theta=formatted_categories_closed,
        mode='lines',
        line=dict(color='Grey', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add main data trace with same fixed category sequence
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=formatted_categories_closed,
        fill='toself',
        name=selected_faculty,
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showline=True,
                linewidth=1,
                linecolor='LightGrey',
                gridcolor='LightGrey',
                gridwidth=1,
                range=[global_min, global_max],
                title='Average Z-Score',
                angle=0,  # Position at bottom
                tickfont=dict(size=12)
            ),
            angularaxis=dict(
                direction='clockwise',
                period=len(formatted_categories)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',    
        showlegend=True,
        title=f"{skill_group} Analysis for {selected_faculty}"

    )
    
    return fig

def create_bar_chart(df):
    """Create a bar chart showing overall faculty performance."""
    avg_scores = df.select_dtypes(include=[np.number]).mean(axis=1)
    fig = px.bar(
        x=avg_scores,
        y=df['Faculty'],
        orientation='h',
        title='Overall Faculty Performance',
        labels={'x': 'Average Z-Score', 'y': 'Faculty'},

    )
    fig.update_layout(
        showlegend=False,
        yaxis={'autorange': 'reversed'},
        )

    return fig

def create_line_chart(df, skill_group):
    """Create a line chart for the selected skill group."""
    metrics = SKILL_GROUPS[skill_group]
    fig = go.Figure()
    
    for metric in metrics:
        fig.add_trace(go.Scatter(
            x=df['Faculty'],
            y=df[metric],
            name=format_metric_name(metric),
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title=f"{skill_group} Comparison Across Faculties",
        xaxis_title="Faculty",
        yaxis_title="Z-Score",
        hovermode='x unified',
        xaxis={'tickangle': -45}
    )
    
    return fig
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