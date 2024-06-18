import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import visualizations


st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


df= pd.read_csv('dubai_properties.csv')

#Drop some useless columns identified in EDA
columns_to_drop = ['Address','Frequency','Purpose','Latitude','Longitude']
df = df.drop(columns_to_drop,axis=1)

#EDA operations
df['Posted_date'] = df['Posted_date'].astype('datetime64[ns]')
df['year'] = df['Posted_date'].dt.year

# Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')
    
    apt_yearly = df.groupby(['year','Type'])['Type'].count().to_frame().rename(columns={'Type':'count'}).reset_index()
    year_list = apt_yearly['year'].unique()
    
    selected_year = st.selectbox('Select a dashboard', year_list)
    