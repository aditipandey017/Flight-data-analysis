import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    layout="wide",
    page_title= "Flight Analysis App",
    page_icon = "✈️",
)

cols_to_drop = ['TailNum','ArrDelay','DepDelay','TaxiIn','TaxiOut','Diverted','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircaftDelay']
rename_dict = {'UniqueCarrier':'Carrier'}

def load_data(path):
    df=pd.read_excel('DelayedFlightsnew.xlsx')   
    df.drop(columns=cols_to_drop, inplace=True)
    df.rename(columns=rename_dict, inplace=True)
    return df

with st.spinner('Processing flight Data.....'):
    df= load_data('DelayedFlightsnew.xlsx')
    
st.image("https://wallpapers.com/images/hd/sunset-silhouette-airplane-brh2gmlmjhnj74dv.jpg", use_column_width=True)
st.title("Flight Data Analysis")

# Flights Frequency

# Busiest airport in terms of Flights arrival 
(df.Origin ).value_counts().head(25).plot(kind='bar')

# Busiest airport in terms of Flights departure
(df.Dest ).value_counts().head(25).plot(kind='bar')

# Popular Routes
df['routes'] = df.Origin+' <-> '+df.Dest
def update_routes(path):
    data =path.split(' <-> ')
    data.sort()
    return " <-> ".join(data)    
df.routes.apply(update_routes).value_counts().head(25).plot(kind='bar')


