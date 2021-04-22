# Module imports
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import pydeck as pdk
from pydeck.types import String
import math


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


def formatChoice(x): return x.replace('_', ' ')


st.markdown('## Dynamic Chart')
variable = st.selectbox(label="Pick a variable", options=list(
    master.columns), format_func=lambda x: x.replace('_', ' '), index=5)
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


st.markdown("## Clustering NPAs")
fieldList = master.columns
fields2017 = list(fieldList[fieldList.to_series().str.endswith(
    '2017') & ~fieldList.to_series().str.contains('moe')])

data = master[fields2017].dropna(axis='columns')

# Streamlit multiselect to pick fields for clustering; => Default ["White_Population_2020"]
clusteringFields = st.multiselect(label='Select fields for clustering',
                                  options=list(data.columns),
                                  format_func=lambda x: x.replace('_', ' '),
                                  default=["White_Population_2017"])
numberOfClusters = st.number_input(
    label="Number of Clusters", min_value=2, max_value=5, value=2)

# If no fields selected, give error
if len(clusteringFields) == 0:
    st.error("Please select one or more fields for clustering NPAs.")
# Else display the clusters and map
else:

    selectedData = data[clusteringFields]
    scaled = normalize(selectedData, axis=0)
    scaled = pd.DataFrame(scaled, columns=selectedData.columns)

    # st.write(selectedData)

    kmeansClusters = KMeans(n_clusters=numberOfClusters, random_state=42)
    kmeansClusters.fit(scaled)

    master['cluster'] = kmeansClusters.labels_ + 1
    master['cluster'] = master['cluster'].astype(int)

    df2 = pd.DataFrame()

    palette = [
        [255, 75, 75, 100],
        [255, 191, 0, 100],
        [47, 114, 255, 100],
        [64, 255, 112, 100],
        [186, 73, 255, 100]
    ]

    def getColor(x):
        if math.isnan(x):
            return [0, 0, 0, 0]
        else:
            return palette[int(x-1)]

    # json = pd.read_json('./qol-data/npa.json')
    jsonData = json.load(open('./qol-data/npa.json'))

    df2['coordinates'] = [feature['geometry']['coordinates']
                          for feature in jsonData['features']]
    df2['NPA'] = [int(feature['properties']['id'])
                  for feature in jsonData['features']]
    df2 = pd.merge(df2, master[["NPA", "cluster"]], on="NPA", how="left")
    df2['fill_color'] = df2['cluster'].map(getColor)
    df2['cluster_tooltip'] = df2['cluster'].map(
        lambda x: 'Cluster {}'.format(int(x)) if x > 0 else '')
    df2 = df2.drop(columns=['cluster'])

    st.markdown('### Cluster 1')
    st.text("NPA: " + str(list(master[master['cluster'] == 1]['NPA'])))
    st.markdown("### Cluster 2")
    st.text("NPA: " + str(list(master[master['cluster'] == 2]['NPA'])))

    view_state = pdk.ViewState(
        **{"latitude": 35.33, "longitude": -80.89, "zoom": 10.50, "maxZoom": 22, "pitch": 0, "bearing": 0}
    )

    beattiesGeoJson = "https://raw.githubusercontent.com/wesmith4/mat210-proj-beatties/main/beatties.geojson"

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        df2,
        opacity=0.8,
        stroked=True,
        get_polygon="coordinates",
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color="fill_color",
        get_line_color=[0, 0, 0],
        lineWidthMinPixels=1,
        auto_highlight=True,
        pickable=True,
    )

    road_layer = pdk.Layer(
        'GeoJsonLayer',
        data=beattiesGeoJson,
        filled=True,
        pickable=False,
        lineWidthMinPixels=2,
        opacity=1,
        id='beatties-ford-road',
        use_binary_transport=False,
        extruded=True
    )

    tooltip = {"html": "<b>NPA:</b> {NPA} <br /><b>{cluster_tooltip}</b>"}

    deck = pdk.Deck(
        layers=[polygon_layer, road_layer],
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        tooltip=tooltip
    )

    st.pydeck_chart(deck)
