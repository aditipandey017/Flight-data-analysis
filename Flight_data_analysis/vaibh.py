import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config(layout="wide",
                   page_title="INDIAN SCHOOL EDUCATION STATISTICS ANALYSIS APP",
                   page_icon='📚')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

# 

rename_dict={"Primary_Total": "Primary", 
             "Upper Primary_Total": "Upper_Primary", 
             "Secondary _Total": "Secondary", 
             "HrSecondary_Total": "HrSecondary"}



@st.cache_data()
def load_data():
    df = pd.read_csv('dropout-ratio-2012-2015.csv')
    india = gpd.read_file('Indian_States.txt')
    df.replace("NR", np.nan, inplace=True)
    df.rename(columns=rename_dict, inplace=True)
    df["Primary"] = df["Primary"].astype(float)
    df["Upper_Primary"] = df["Upper_Primary"].astype(float)
    df["Secondary"] = df["Secondary"].astype(float)
    df["HrSecondary"] = df["HrSecondary"].astype(float)
    df_total = df[['Primary','Upper_Primary','Secondary','HrSecondary']]
    df["Average"] = df_total.mean(axis=1)
    return df, india
 

with st.spinner("Processing Immigration data...."):
    df, india = load_data()

num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(include='object').columns


c1, c2 = st.columns([3,1])
c1.image('https://mcmscache.epapr.in/post_images/website_350/post_29811255/full.jpg', use_column_width=True)
c1.title('Indian School Education Statistics Analysis')
c1.markdown("""
* **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn, geopandas
* **Data source:** [Indian School Education Statistics](https://data.gov.in/resources/stateut-wise-average-annual-drop-out-rate-2012-13-2014-15-ministry-human-resource
""")


states = df["State_UT"].unique()
c1, c2 = st.columns(2)
c1.subheader("Select the state to visualize the dropout rates")
state = c1.selectbox("State", states)
df_state = df[df["State_UT"] == state]
c1.dataframe(df_state, use_container_width=True)
col = c1.selectbox("Select the level to visualize the dropout rates", num_cols)
c2.subheader("Line chart of dropout rates for each level")
fig, ax = plt.subplots(figsize=(10,7))
sns.barplot(x="year", y=col, data=df_state, ax=ax)
c2.pyplot(fig, use_container_width=True)


c2.info("Raw dataset")
c2.dataframe(df, use_container_width=True)
# df["year"] = pd.to_numeric(df["year"], errors="coerce")
df_grouped = df.groupby("year")[num_cols].mean().reset_index()
merged = pd.merge(india, df, left_on="NAME_1", right_on="State_UT", how="inner")
merged =merged[merged['NAME_1'] != 'Chandigarh']

st.header('Dropout Analysis and Visualization')

c1, c2 = st.columns(2)
c1.subheader('Average Dropout Rates in India from 2012 to 2015')
fig, ax = plt.subplots(1, 1, figsize=(20, 20))  # Increase the figsize to increase the size of the map
merged.plot(column='Average', cmap='YlOrBr', linewidth=1, ax=ax, edgecolor='0.5', legend=True)
for idx, row in merged.iterrows():
    centroid_x, centroid_y = row['geometry'].centroid.x, row['geometry'].centroid.y
    state_name = row['NAME_1']
    ax.text(centroid_x, centroid_y, state_name, fontsize=10, ha='center', va='center')
c1.pyplot(fig, use_container_width=True)

c2.subheader('Correlation Matrix between Dropout Rates for each level')
df_total = df[['Primary','Upper_Primary','Secondary','HrSecondary']]
fig,ax=plt.subplots(figsize=(10,9))
sns.heatmap(df_total.corr(), annot=True, cmap="Blues", ax=ax)
ax.set_title("Correlation matrix of dropout rates for each level")
c2.pyplot(fig, use_container_width=True)

# Plotting the pairplot
st.subheader('Pairplot of Dropout Rates')
fig = sns.pairplot(df_total, corner=True)
st.pyplot(fig)

c1, c2 = st.columns(2)
# Sort the dataframe by the average dropout rate in ascending order
df_sorted = df.sort_values(by="Average", ascending=True)
# Select the first five rows for the best states
df_best5 = df_sorted.head(5)
# Select the last five rows for the worst states
df_worst5 = df_sorted.tail(5)
# Concatenate the best and worst states into a new dataframe
df_comparison = pd.concat([df_best5, df_worst5])
data = df_best5["Average"]
labels = df_best5["State_UT"]
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(data, labels=labels, autopct="%.1f%%", wedgeprops=dict(width=0.4),
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ff6633', '#ffccff'],
        textprops={'fontsize': 12}, labeldistance=1.05, pctdistance=0.8)
ax.set_title("Pie chart of the top 5 best states in terms of dropout rates")
ax.axis("equal")
c1.pyplot(fig)


# Extract the data and labels for the pie chart
data = df_worst5["Average"]
labels = df_worst5["State_UT"]
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(data, labels=labels, autopct="%1.1f%%", 
       colors=['#ff9999', '#66b3ff', '#99ff99', '#99ffAA', '#ff6633'],
        wedgeprops=dict(width=0.4), textprops={'fontsize': 12}, labeldistance=1.05, pctdistance=0.8)
ax.set_title("Pie chart of the top 5 worst states in terms of dropout rates")
ax.axis("equal")

# Show the pie chart using Streamlit
c2.pyplot(fig)


c1, c2 = st.columns(2)
df_boys=df[["Primary_Boys","Upper Primary_Boys","Secondary _Boys","HrSecondary_Boys"]]
df_girls=df[["Primary_Girls","Upper Primary_Girls","Secondary _Girls","HrSecondary_Girls"]]
df_boys = df_boys.apply(pd.to_numeric, errors='coerce')
df_girls=df_girls.apply(pd.to_numeric, errors='coerce')
# Calculate the total dropout rates for boys and girls
boys_total = df_boys.sum().sum()
girls_total = df_girls.sum().sum()

# Calculate the percentage of dropout rates for boys and girls
boys_percentage = (boys_total / (boys_total + girls_total)) * 100
girls_percentage = (girls_total / (boys_total + girls_total)) * 100

# Create a pie chart to visualize the comparison
labels = ['Boys', 'Girls']
sizes = [boys_percentage, girls_percentage]
colors = ['#ff9999', '#66b3ff']
st.title('Comparison of Dropout Rates between Boys and Girls')
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(sizes, labels=labels, colors=colors, autopct='%.1f%%', startangle=90,
        textprops={'fontsize': 12}, wedgeprops=dict(width=0.4), pctdistance=0.8, labeldistance=1.05)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
c1.pyplot(fig)



# Calculate the total dropout rates for each level
primary_total = df["Primary"].sum()
upper_primary_total = df["Upper_Primary"].sum()
secondary_total = df["Secondary"].sum()
hrsecondary_total = df["HrSecondary"].sum()


st.write("Total Dropout Rates:")
st.write("Primary:", primary_total)
st.write("Upper Primary:", upper_primary_total)
st.write("Secondary:", secondary_total)
st.write("Higher Secondary:", hrsecondary_total)