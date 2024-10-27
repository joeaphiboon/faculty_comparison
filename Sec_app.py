import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


# Page configuration
st.set_page_config(
    page_title="Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Define skill groups
SKILL_GROUPS = {
    'Core Skills': [
        'avg Self-Awareness',
        'avg Confidence',
        'avg Positive Attitude',
        'avg Communication',
        'avg Creativity',
        'avg Global Competence'
    ],
    'Communication Cluster': [
        'avg Communication',
        'Encode',
        'Decode',
        'Plan',
        'Communicationandcollaboration'
    ],
    'Leadership Cluster': [
        'Leadershipandprojectmanagement',
        'Criticalthinkingandproblemsolving',
        'Criticalthinking',
        'Self-confidence',
        'Initiative',
        'Showdedication',
        'Responsibilitytaking'
    ],
    'Global Cluster': [
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
    # Add spaces before capital letters
    name = ''.join([' ' + c if c.isupper() else c for c in name]).strip()
    # Replace 'and' with '&'
    name = name.replace(' and ', ' & ')
    return name.title()

def load_data():
    """Load data from different sources."""
    # First try to load from secrets
    try:

        # Check if secrets exist
        if not hasattr(st, 'secrets'):
            st.sidebar.warning("No secrets configuration found")
            raise Exception("No secrets configuration")
            

        if "general" not in st.secrets:
            st.sidebar.warning("No 'general' section in secrets")
            raise Exception("No 'general' section")
            
        if "data" not in st.secrets["general"]:
            st.sidebar.warning("No 'data' key in general section")
            raise Exception("No 'data' key")
        
        # Try to parse the JSON data
        try:
            df = pd.read_json(st.secrets["general"]["data"])
            #st.sidebar.success("✅ Data successfully loaded from secrets")
            return df
        except Exception as e:
            st.sidebar.error(f"Error parsing JSON data: {str(e)}")
            raise Exception(f"JSON parsing error: {str(e)}")
            
    except Exception as e:
        st.sidebar.warning(f"Failed to load from secrets: {str(e)}")
        
        # Fallback to local file
        try:
            st.sidebar.info("Attempting to load from local file...")
            df = pd.read_csv('Faculty_Comparison_of_Z-Scores.csv')
            #st.sidebar.success("✅ Data loaded from local file")
            return df
        except Exception as e:
            st.sidebar.error(f"Error loading local file: {str(e)}")
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
                tickfont=dict(size=12),
                # Force specific tick values to ensure we get a line at zero
                tickvals=np.linspace(global_min, global_max, 5),  # 5 ticks including min and max
                ticktext=[f"{x:.1f}" for x in np.linspace(global_min, global_max, 5)],
                
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
    st.title("Performance Analysis Dashboard")
    st.text('v.1.0.1 : by JTIAPBN.Ai')
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Unable to load data. Please check configuration.")
        st.stop()
    
    # Sidebar
    st.sidebar.title("Dashboard Controls")
    selected_faculty = st.sidebar.selectbox(
        "Select Faculty",
        df['Faculty'].tolist()
    )
    
    selected_group = st.sidebar.selectbox(
        "Select Skill Group",
        list(SKILL_GROUPS.keys())
    )
    
    # Main layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar Chart
        st.plotly_chart(
            create_radar_chart(df, selected_faculty, selected_group),
            use_container_width=True
        )
    
    with col2:
        # Bar Chart
        st.plotly_chart(
            create_bar_chart(df),
            use_container_width=True
        )
    
    # Line Chart (full width)
    st.plotly_chart(
        create_line_chart(df, selected_group),
        use_container_width=True
    )
    
    # Additional information
    with st.expander("About the Metrics"):
        st.write("""
        This dashboard presents faculty performance analysis based on various skill groups:
        
        1. **Core Skills**: Fundamental 6 Core Skills including self-awareness, confidence, positive attitude, communication, creativity, and global competence
        2. **Communication Cluster***: Communication-related skills including communication, encode, decode, plan, and dommunication and colaboration. 
        3. **Leadership Cluster***: Leadership and management-related skills including leadership and project management, critical thinking and problem solving, critical thinking, self-confidence, initiative, show dedication, and responsibility taking.
        4. **Global Cluster***: Cultural and global awareness-related skills including global competence, global citizen, intercultural awareness, open-minded, exploration and openness to new perspectives, collaboration and collective creativity, emotions, personal growth, and self-reflection.
        
        *Clusters are based on PISA definitions and Peason correlation analysis.\n
        All metrics are presented as Z-scores, representing standard deviations from the mean.
        """)

if __name__ == "__main__":
    main()
