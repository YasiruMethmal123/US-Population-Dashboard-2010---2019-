import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from PIL.ImageColor import colormap
from numpy.ma.core import zeros
from pandas import wide_to_long
from streamlit import title

# Configure Streamlit page
st.set_page_config(
    page_title="US Population Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable Altair dark theme
alt.themes.enable("dark")

# Sample data (replace with pd.read_csv('data/20102019population.csv') when using actual data)

df_reshaped = pd.read_csv('./data/20102019population.csv')

#Verifing required columns
required_columns = ['states' , 'year' , 'population']
if not all(col in df_reshaped.columns for col in required_columns):
    st.error(f"Error CSV must contain the columns : {', '.join(required_columns)}")
    st.stop()

#Ensure Year is integer and population is numaric
df_reshaped['year'] = df_reshaped['year'].astype(int)
df_reshaped['population'] = pd.to_numeric(df_reshaped['population'] , errors = 'coerce')

#Dashboard Title
st.title("US Population Dashboard (2010 - 2019)")

#Sidebar for state search and filters
st.sidebar.header("Search and Filters")
state_options = sorted(df_reshaped["states"].unique())
selected_states = st.sidebar.multiselect(
    "Search States",
    options=state_options,
    default=[state_options[0]] if state_options else [],
    help="Select one or more states to display data"
)
#Filter with year
min_year = int(df_reshaped['year'].min())
max_year = int(df_reshaped['year'].max())
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year,max_year),
    help="Adjust the year range for the data"
)
#Filter data based on selection
filterd_df = df_reshaped[
    (df_reshaped['states'].isin(selected_states))&
    (df_reshaped['year'].between(selected_years[0] , selected_years[1]))
]

if not selected_states:
    st.warning("Please select at least one state to display data")
else:
    col1 , col2 = st.columns(2)

    with col1:
        st.subheader("Population Trend by State")
        line_chart = alt.Chart(filterd_df).mark_line(point =True).encode(
            x = alt.X('year:O' , title = 'Year'),
            y = alt.Y('population:Q' , title = 'Population' ,scale = alt.Scale(zero = False)),
            color = 'states:N',
            tooltip = ['states' , 'year' , 'population']
        ).properties(
            width = 600,
            height = 400,
            title = "Population Trend (2010=2019)"
        )
        st.altair_chart(line_chart,use_container_width=True)

    with col2:
        st.subheader(f"Population in {selected_years[1]}")
        bar_df = filterd_df[filterd_df['year'] == selected_years[1]]
        fig = px.bar(
            bar_df,
            x = 'states',
            y = 'population',
            color = 'states',
            title = f"Population by state in {selected_years[1]}",
            width = 600,
            height = 400
    )
    st.plotly_chart(fig,use_container_width=True)

#Summery statistic
st.subheader("Summery Statistics")
summary = filterd_df.groupby('states').agg({
    'population': ['mean', 'min', 'max']
}).round(0).astype(int)
summary.columns = ['Average Population', 'Min Population', 'Max Population']
st.dataframe(summary , use_container_width=True)

#Display filtered data table
st.subheader("Filtered Table")
st.dataframe(filterd_df[['states' , 'year' , 'population']],use_container_width=True)