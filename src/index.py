# import streamlit as st
# import pandas as pd
# import altair as alt
# import plotly.express as px
#
# ##Configuring Page
# st.set_page_config(
#     page_title= "US Population Dashboard",
#     layout= "wide",
#     initial_sidebar_state="expanded"
# )
# alt.themes.enable("dark")
#
# # df_reshaped = pd.read_csv('data/20102019population.csv')
#
#
from gc import collect
from idlelib.iomenu import errors
from operator import index
from xxlimited_35 import error

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

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

