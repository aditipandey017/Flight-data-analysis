#import the libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(
    layout="wide",
    page_title= "Flight Data Analysis",
    page_icon = "✈️",
)

def dep_delay_in_minute(scheduled, actual):
    t1 = datetime.strptime(scheduled, "%H:%M")
    t2 = datetime.strptime(actual, "%H:%M")
    delta = t2 - t1
    ms = delta.total_seconds() / 60
    return ms

def generate_readable_time(data):
    if isinstance(data, int):
        data = list(str(data))
        if len(data) == 4:
            data = f"{data[0]}{data[1]}:{data[2]}{data[3]}"
        elif len(data) == 3:
            data = f"0{data[0]}:{data[1]}{data[2]}"
        elif len(data) == 2:
            data = f"00:{data[0]}{data[1]}"
        elif len(data) == 1:
            data = f"00:0{data[0]}"
        else:
            print(data)
        return data

def update_routes(path):
    data =path.split(' <-> ')
    data.sort()
    return " <-> ".join(data)    

cols_to_drop = ['TailNum','ArrDelay','DepDelay','TaxiIn','TaxiOut','Diverted','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircaftDelay']
rename_dict = {'UniqueCarrier':'Carrier',
               'Flightcode':'Number of Flight'}

@st.cache_data()
def load_data(path):
    df=pd.read_excel('DelayedFlightsnew.xlsx')   
    df.drop(columns=cols_to_drop, inplace=True)
    df.rename(columns=rename_dict, inplace=True)
    df['DepDelay']= df['DepTime']-df['CRSDepTime']
    df['ArrDelay']= df['ArrTime']-df['CRSArrTime']
    df['DepTime'].apply(generate_readable_time)
    df['CRSDepTime'].apply(generate_readable_time)
    df['CRSArrTime'].apply(generate_readable_time)               
    df['DepTime']= df['DepTime'].apply(generate_readable_time)
    df['CRSDepTime']=df['CRSDepTime'].apply(generate_readable_time)
    df['ArrTime']=df['ArrTime'].apply(generate_readable_time)
    df['CRSArrTime']=df['CRSArrTime'].apply(generate_readable_time)
    df.loc[df.DepDelay.isna(), "dep_status"]="Cancelled"
    df.loc[df.DepDelay <= 0, "dep_status"]="OnTime"
    df.loc[df.DepDelay > 0, "dep_status"]="Late"
    df.loc[df.ArrDelay.isna(), "arr_status"]="Cancelled"
    df.loc[df.ArrDelay <= 0, "arr_status"]="OnTime"
    df.loc[df.ArrDelay > 0, "arr_status"]="Late"
    return df

with st.spinner('Processing flight Data.....'):
    df= load_data('DelayedFlightsnew.xlsx')

st.image("https://wallpapers.com/images/hd/sunset-silhouette-airplane-brh2gmlmjhnj74dv.jpg", use_column_width=True)
st.title("Flight Data Analysis")

#Dataset information
st.header("Basic Information about the flight dataset")
Number_of_Flight = df.shape[0]
year= "2018"

c1,c2,c3= st.columns(3)
c1.metric("Total Flights",Number_of_Flight)
c2.metric("Year of Data",year)
c3.metric('Total Fields', df.shape[1])

columns = df.columns.tolist()
num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = df.select_dtypes(include='object').columns.tolist()
col_str = ", ".join(columns)
c4,c5,c6= st.columns(3)
c4.subheader("total columns")
c4.write(col_str)
c5.subheader("numerical columns")
c5.write(", ".join(num_cols))
c6.subheader("categorical columns")
c6.write(", ".join(cat_cols))

t1, t2, t3 = st.tabs(['All Data', 'Numerical Stats', 'Categorical Stats'])
with t1:
    st.dataframe(df, use_container_width=True)    
with t2:
    st.dataframe(df.describe(), use_container_width=True)    
with t3:
    st.dataframe(df.describe(include='object'), use_container_width=True) 

st.title("Analysis and Visualization Section")
# Flights Frequency
#Popular routes
st.header("Popular Routes")
df['routes'] = df.Origin+' <-> '+df.Dest
routes_series = df.routes.apply(update_routes).value_counts()
size = st.slider("How many values for origin-destination", min_value=5, max_value=50, step=5)
routes_series = routes_series.head(size)
fig = px.bar(routes_series, 
             routes_series.values,
            routes_series.index, title="ROutes", height=500,
            color_discrete_sequence=['orange'])
st.plotly_chart(fig, use_container_width=True,)
st.write('LGA<->ORD is the most popular route.')

#Flights Arrival and Departure Status
st.header("Flights Arrival and Departure Status")
c1, c2 = st.columns(2)
ArrStatus=df.groupby(['arr_status'])['arr_status'].count()
fig= px.pie(ArrStatus,ArrStatus.index, ArrStatus.values, title ='Arrival Status')
c1.plotly_chart(fig, use_container_width=True)
DepStatus=df.groupby(['dep_status'])['dep_status'].count()
fig= px.pie(DepStatus,DepStatus.index, DepStatus.values,title ='Departure status')
c2.plotly_chart(fig, use_container_width=True)

# Flights frequency across months
st.header("Flights frequency across months")
buzMonth = df.groupby(['Month'])['Month'].count()
flight_freq = df.Month.value_counts()
fig= px.funnel(flight_freq, flight_freq.index,flight_freq.values,
                color_discrete_sequence=['teal'])
st.plotly_chart(fig, use_container_width=True,)
st.write('Flights frequency is highest in July and lowest in December.')

# Busiest Aircraft in terms of Flights Arrival and Departure
c1, c2 = st.columns(2)
c1.subheader('Busiest Aircraft in terms of Flights Arrival')
# Flights Arrival Status
origin_series = df.Origin.value_counts()
size = c1.slider("How many values for origin", min_value=5, max_value=50, step=5)
origin_series = origin_series.head(size)
fig = px.bar(origin_series, origin_series.index, 
             origin_series.values, title="Origin",
             color_discrete_sequence=['purple'])
c1.plotly_chart(fig, use_container_width=True)
# Flights Departure Status
c2.subheader('Busiest airport in terms of Flights departure')
dest_series = df.Dest.value_counts()
size = c2.slider("How many values for destination", min_value=5, max_value=50, step=5)
dest_series = dest_series.head(size)
fig = px.bar(dest_series, dest_series.index, 
             dest_series.values, title="Destinations",
             color_discrete_sequence=['pink'])
c2.plotly_chart(fig, use_container_width=True,)
st.write('ORD is the busiest airport with with 25.4% of total flights arrived at this airport and 28.6% of total flights departed from this airport')

# Best and worst carrier w.r.t total flight cancelled
st.header("Best and worst carrier w.r.t total flight cancelled")
carriers =  df.loc[df['arr_status'] == 'Cancelled'].groupby(['Carrier'])['arr_status'].count()
c1,c2 = st.columns([3,7])
c1.dataframe(carriers, use_container_width=True)# fig = px.pie(carriers)
fig = px.pie(carriers, carriers.index, carriers.values, hole=.4, height=500 )
c2.plotly_chart(fig, use_container_width=True)
st.write('AA and OH are the best and worst carriers in terms of flight cancellation')

# Best and worst Airport w.r.t total flight cancelled
st.header("Best and worst Airport w.r.t total flight cancelled")
bwAir=df.loc[df['arr_status'] == 'Cancelled'].groupby(['Origin'])['arr_status'].count()
fig= px.line(bwAir,
             bwAir.index,
             bwAir.values,
             color_discrete_sequence=['yellow'])
st.plotly_chart(fig, use_container_width=True)
st.write('Total flight got canceled at ORD airport is highest among all.')

# Flight cancellation across months
st.header("Flight cancellation across months")
MonthCancel=df.loc[df['arr_status'] == 'Cancelled'].groupby(['Month'])['arr_status'].count()
c1,c2 = st.columns(2)
fig= px.funnel_area(MonthCancel,
             MonthCancel.index,
             MonthCancel.values,
)
c1.plotly_chart(fig, use_container_width=True)
fig=px.scatter(MonthCancel,
             MonthCancel.index,
             MonthCancel.values,
             title= 'Scatter plot representation'
)
c2.plotly_chart(fig, use_container_width=True)
st.write('Flight cancellation is lowest in September month')                    ##########################

# Best and worst airport in terms of departure and arrival delay
st.header('Best and worst airport in terms of arrival and departure delay')
arrdelayed = df[df["ArrDelay"] > 0]
c1,c2 = st.columns(2)
# Create a pairplot chart
fig = px.scatter_matrix(
    arrdelayed,
    dimensions=["ArrDelay"],
   )
c1.plotly_chart(fig, use_container=True)
depdelayed = df[df["DepDelay"] > 0]
fig = px.scatter_matrix(
    depdelayed,
    dimensions=["DepDelay"],
   )
c2.plotly_chart(fig, use_container=True)

st.header('Delayed Flight across month')
# Group data by month and calculate the total number of delayed flights
delayed_flights_by_month = df.groupby("Month")["DepDelay"].sum()
fig= px.pie(delayed_flights_by_month,delayed_flights_by_month.index, delayed_flights_by_month.values,
            hole=.5, height=500
            )
st.plotly_chart(fig, use_container_width=True)
st.write('Flights delay is more in July month, where as June has minimum flight delays.')

# Flight speed
st.header('Average flight speed across all carriers')
df['Speed'] = df['Distance']/(df['ActualElapsedTime']/60)
# Average flight speed across all carriers
flightSpeed = df.groupby(['Carrier'])['Speed'].mean()
fig= px.bar(flightSpeed,flightSpeed.index, flightSpeed.values,
            color_discrete_sequence=['yellowgreen'])
st.plotly_chart(fig, use_container_width=True)
st.write('F9 is best in terms of average flight speed with 362 miles/hr')

st.title('Conclusion:')
st.subheader('In 2018, around 87% of flight got delayed and most of them were in July, August and September months, where as June and December are the best month to travel. From flight frequency graph we can see that air traffic is more in these 3 months, So this is the reason flights got delayed in July, August and September months.')
