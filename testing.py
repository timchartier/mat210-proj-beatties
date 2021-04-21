import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans


dataFrames = {
    'Character': 'character',
    'Economy': 'economy',
    'Education': 'education',
    'Engagement': 'engagement',
    'Environment': 'environment',
    'Health': 'health',
    'Housing': 'housing',
    'Safety': 'safety',
    'Transportation': 'transportation'
}


def getDataFrame(topic):
    return pd.read_pickle('./qol-data/pickles/{}.pkl'.format(topic))


# Read in master data frame from pickle file
master = pd.read_pickle('./qol-data/master.pkl')
# Read in variable metadata from csv file
metadata = pd.read_csv('./qol-data/csvFiles/metadata.csv')

df = getDataFrame(dataFrames['Economy'])
df[['Household_Income_2017', 'Household_Income_2018']] = df[[
    'Household_Income_2017', 'Household_Income_2018']].astype(float)
master[['Household_Income_2017', 'Household_Income_2018']] = master[[
    'Household_Income_2017', 'Household_Income_2018']].astype(float)


def formatChoice(x): return x.replace('_', ' ')


st.markdown('## Dynamic Chart')
variable = st.selectbox(label="Pick a variable", options=list(
    master.columns), format_func=lambda x: x.replace('_', ' '))
description = metadata[metadata['Long_Name']
                       == variable]['Long_Description'].values[0]
st.write(description)

st.write(master[variable])

fig2 = px.bar(master, x=variable, y="order", orientation="h",
              labels=dict(variable=formatChoice(variable), order="NPA"))
fig2.update_yaxes(autorange="reversed",
                  ticktext=master.NPA.tolist(), tickvals=master.order.to_list())
st.plotly_chart(fig2)

# Construct dataframe for population by race
data = master[['NPA', 'order', 'Population _2018', 'White_Population_2018',
               'Black_Population_2018', 'Asian_Population_2018', 'Hispanic_Latino_2018', 'All_Other_Races_2018']]
data.columns = ['NPA', 'order', 'Total Population',
                'White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']
data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']
     ] = data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']].astype(float)
data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']] = data[['White', 'Black',
                                                                      'Asian', 'Hispanic/Latino', 'Other']].multiply(data['Total Population'], axis="index")/100

melted = pd.melt(data, id_vars=['NPA', 'order'], value_vars=[
                 'White', 'Black', 'Asian', 'Hispanic/Latino', 'Other'], var_name="Race", value_name="population")

fig3 = px.bar(melted, y="order", x="population", color="Race",
              orientation="h", labels=dict(order="NPA", population="Population"), title="Population by Race")
fig3.update_yaxes(autorange="reversed",
                  ticktext=data.NPA.tolist(), tickvals=data.order.to_list())

st.plotly_chart(fig3)

fieldList = master.columns
fields2017 = list(fieldList[fieldList.to_series().str.endswith(
    '2017') & ~fieldList.to_series().str.contains('moe')])

data = master[fields2017].dropna(axis='columns')

clusteringFields = st.multiselect(label='Select fields for clustering',
                                  options=data.columns, format_func=lambda x: x.replace('_', ' '))

selectedData = data[clusteringFields]
scaled = normalize(selectedData, axis=0)
scaled = pd.DataFrame(scaled, columns=selectedData.columns)

st.write(selectedData)
st.write(scaled)

kmeansClusters = KMeans(n_clusters=2)
kmeansClusters.fit(scaled)

st.write(kmeansClusters.labels_)
