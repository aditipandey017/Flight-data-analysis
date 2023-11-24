import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    layout="wide",
    page_title= "Flight Analysis App",
    page_icon = "✈️",
)

cols_to_drop = ['TailNum','ArrDelay','DepDelay','TaxiIn','TaxiOut','Diverted','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircaftDelay']
rename_dict = {'UniqueCarrier':'Carrier'}

def load_data(path):
    df=pd.read_excel('DelayedFlightsnew.xlsx', sheet_name=1, skiprows=20, skipfooter=2)   
    df.drop(columns=cols_to_drop, inplace=True)
    df.rename(columns=rename_dict, inplace=True)
    return df

with st.spinner('Processing Immigration Data.....'):
    df= load_data('DelayedFlightsnew.xlsx')
    
st.image("https://wallpapers.com/images/hd/sunset-silhouette-airplane-brh2gmlmjhnj74dv.jpg", use_column_width=True)
st.title("Immigration Analysis App")
