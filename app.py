import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# App configuration
st.set_page_config(
    page_title="Climate Research Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    temp_data = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
    temp_data = temp_data[temp_data['country'] == 'World']
    temp_data['year'] = pd.to_datetime(temp_data['year'], format='%Y')
    return temp_data

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=1750,
    max_value=2020,
    value=(1900, 2020)
)

# Bio Section
st.title("Climate Change Research Dashboard")
st.header("About Me")
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=150)
with col2:
    st.write("""
    **Name**: Data Researcher  
    **Affiliation**: Climate Studies Institute  
    **Research Interests**: 
    - Global temperature trends
    - CO₂ emissions impact
    - Climate change mitigation strategies
    
    This dashboard showcases key indicators of climate change over time.
    """)

# Main content
st.header("Key Climate Indicators")

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("CO₂ Concentration (2020)", "414 ppm", "+2.5 ppm from 2019")
col2.metric("Global Temperature Anomaly", "+1.2°C", "Above pre-industrial")
col3.metric("Sea Level Rise", "3.7 mm/year", "Accelerating")

# Graphs section
st.subheader("Historical Trends")

tab1, tab2, tab3 = st.tabs(["CO₂ Emissions", "Temperature Change", "Combined View"])

with tab1:
    fig1 = px.line(
        df[(df['year'].dt.year >= start_year) & (df['year'].dt.year <= end_year)],
        x='year',
        y='co2',
        title='Global CO₂ Emissions Over Time',
        labels={'co2': 'CO₂ Emissions (million tonnes)', 'year': 'Year'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.line(
        df[(df['year'].dt.year >= start_year) & (df['year'].dt.year <= end_year)],
        x='year',
        y='temperature_change_from_co2',
        title='Temperature Change from CO₂',
        labels={'temperature_change_from_co2': 'Temperature Change (°C)', 'year': 'Year'}
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df['year'],
        y=df['co2'],
        name='CO₂ Emissions',
        yaxis='y1'
    ))
    fig3.add_trace(go.Scatter(
        x=df['year'],
        y=df['temperature_change_from_co2'],
        name='Temperature Change',
        yaxis='y2'
    ))
    fig3.update_layout(
        title='CO₂ and Temperature Correlation',
        yaxis=dict(title='CO₂ (million tonnes)'),
        yaxis2=dict(
            title='Temperature Change (°C)',
            overlaying='y',
            side='right'
        )
    )
    st.plotly_chart(fig3, use_container_width=True)

# Data table section
st.subheader("Raw Data")
st.dataframe(
    df[(df['year'].dt.year >= start_year) & (df['year'].dt.year <= end_year)].sort_values('year', ascending=False),
    column_config={
        "year": st.column_config.DateColumn("Year"),
        "co2": st.column_config.NumberColumn("CO₂ (mt)"),
        "temperature_change_from_co2": st.column_config.NumberColumn("Temp Change (°C)")
    },
    hide_index=True,
    use_container_width=True
)

# Footer
st.markdown("---")
st.caption("""
    Data Source: Our World in Data (https://github.com/owid/co2-data)  
    Dashboard created with Streamlit
""")