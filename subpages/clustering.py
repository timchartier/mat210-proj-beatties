# Module imports
from altair.vegalite.v4.api import value
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


def run():
    with st.beta_container():
        st.title('Clustering neighborhoods along Beatties Ford Road')
    st.markdown("""
    Here, we cluster Neighborhood Profile Areas (NPAs) according to characteristics of your choosing.

    As defined by the [Quality of Life Study](https://mcmap.org/qol/#15/):

    > *Neighborhood Profile Areas (NPAs) are geographic areas used for the organization and presentation of data in the Quality of Life Study.
    The boundaries were developed with community input and are based on one or more Census block groups.*

    """)

    # Read in master data frame from pickle file
    master = pd.read_pickle('./qol-data/master.pkl')
    # Read in variable metadata from csv file
    metadata = pd.read_csv('./qol-data/csvFiles/metadata.csv')

    # Read in metadata lookup file
    variableLookup = pd.read_csv('./qol-data/variableLookup.csv')

    def formatChoice(x): return x.replace('_', ' ')

    st.markdown('## Dynamic Chart')
    variable = st.selectbox(label="Pick a variable", options=list(
        master.columns), format_func=lambda x: x.replace('_', ' '), index=5)
    varCode = variableLookup[variableLookup['name'] == variable]['code'].values[0]
    description = metadata[metadata['Short _Name'] == varCode]['Long_Description'].values[0]
    st.write(description)

    # st.write(master[variable])

    fig2 = px.bar(master, x=variable, y="order", orientation="h",
                  labels=dict(variable=formatChoice(variable), order="NPA"))
    fig2.update_yaxes(autorange="reversed",
                      ticktext=master.NPA.tolist(), tickvals=master.order.to_list())
    st.plotly_chart(fig2)

    # # Construct dataframe for population by race
    # data = master[['NPA', 'order', 'Population _2018', 'White_Population_2018',
    #                'Black_Population_2018', 'Asian_Population_2018', 'Hispanic_Latino_2018', 'All_Other_Races_2018']]
    # data.columns = ['NPA', 'order', 'Total Population',
    #                 'White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']
    # data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']
    #      ] = data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']].astype(float)
    # data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']] = data[['White', 'Black',
    #                                                                       'Asian', 'Hispanic/Latino', 'Other']].multiply(data['Total Population'], axis="index")/100

    # melted = pd.melt(data, id_vars=['NPA', 'order'], value_vars=[
    #     'White', 'Black', 'Asian', 'Hispanic/Latino', 'Other'], var_name="Race", value_name="population")

    # fig3 = px.bar(melted, y="order", x="population", color="Race",
    #               orientation="h", labels=dict(order="NPA", population="Population"), title="Population by Race")
    # fig3.update_yaxes(autorange="reversed",
    #                   ticktext=data.NPA.tolist(), tickvals=data.order.to_list())

    # st.plotly_chart(fig3)

    # Section on clustering
    st.markdown("## Clustering NPAs")
    usableData = master.dropna(axis='columns').drop(columns=['NPA', 'order'])

    data = master[list(usableData.columns)].dropna(axis='columns')

    variablePresets = {
        'Demographic': ["White_Population_2017","Black_Population_2017","Asian_Population_2017","Hispanic_Latino_2017","All_Other_Races_2017"],
        'Education': ['Proficiency_Elementary_School_2017','Proficiency_Middle_School_2017','High_School_Diploma_2017','Bachelors_Degree_2017', 'Early_Care_Proximity_2017'],
        'Health Resources Proximity': ['Low_Cost_Healthcare_Proximity_2018','Pharmacy_Proximity_2018','Grocery_Proximity_2018'],
        'Transportation': ['Long_Commute_2018','Bicycle_Friendliness_2018','Street_Connectivity_2018','Sidewalk_Availability_2015','Transit_Proximity_2018'],
        'Engagement': ['Arts_Participation_2013','311_Requests_2016','Voter_Participation_2018',],
        'Environment': ['Tree_Canopy_2012','Residential_Tree_Canopy_2012','Impervious_Surface_2018','Natural_Gas_Consumption_2013','Water_Consumption_2018','Commuters_Driving_Alone_2018',],
        'Housing': ['Housing_Density_2019','Single_Family_Housing_2019','Housing_Size_2019','Housing_Age_2019','Rental_Houses_2018','New_Residential_2018','Residential_Renovation_2018','Home_Sales_Price_2015','Home_Ownership_2018','Residential_Occupancy_2018','Rental_Houses_2017',],
        'Crime': ['Violent_Crime_Rate_2018','Property_Crime_Rate_2018','Disorder_Call_Rate_2018',]
    }

    whichPreset = st.selectbox(
        label="Use preselected sets of variables",
        options=list(variablePresets.keys()),
        index=0
    )

    with st.beta_container():
        # Streamlit multiselect to pick fields for clustering; => Default ["White_Population_2020"]
        col1, col2 = st.beta_columns((4, 1))
        clusteringFields = col1.multiselect(label='Or, select specific fields for clustering (or add on to the presets!)',
                                            options=list(usableData.columns),
                                            format_func=lambda x: x.replace(
                                                '_', ' '),
                                            default=variablePresets[whichPreset],
                                            help="Choose from the dropdown, or type to search.")
        with st.beta_expander("Variable Descriptions"):
            for var in clusteringFields:
                varCode = variableLookup[variableLookup['name'] == var]['code'].values[0]
                description = metadata[metadata['Short _Name'] == varCode]['Long_Description'].values[0]
                st.markdown("""
                - `{}`: {}
                """.format(var, description))
        st.empty()

    numberOfClusters = col2.number_input(
        label="Number of Clusters", min_value=2, max_value=5, value=2,help="Min: 2, Max: 5")

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

        def getClusterColor(x): return palette[x]

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

        # Summary of data by cluster
        st.markdown('### Averages by Cluster')
        summary = master.groupby('cluster').mean()[clusteringFields]
        summary['Cluster'] = summary.index.map(
            lambda x: 'Cluster {}'.format(x))
        summary = summary[['Cluster'] + clusteringFields]

        def getSummaryColor(row):
            ind = int(row.Cluster.split(' ')[1]) - 1
            colorCode = palette[ind]
            return ['background-color: rgba({},{},{},.3)'.format(colorCode[0], colorCode[1], colorCode[2], colorCode[3])]*(1+len(clusteringFields))
        summary = summary.style.apply(getSummaryColor, axis=1)
        st.write(summary)

        # for cluster in range(numberOfClusters):
        #     st.markdown('### Cluster {}'.format(cluster+1))
        #     st.text(
        #         "NPA: " + str(list(master[master['cluster'] == cluster+1]['NPA'])))

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
            lineWidthMinPixels=3,
            get_line_color=[0,0,200],
            opacity=1,
            id='beatties-ford-road',
            use_binary_transport=False,
            extruded=True
        )

        tooltip = {"html": "<b>NPA:</b> {NPA} <br /><b>{cluster_tooltip}</b>"}

        deck = pdk.Deck(
            layers=[polygon_layer, road_layer],
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=view_state,
            tooltip=tooltip
        )

        st.pydeck_chart(deck)

        # View variables on NPA map
        st.markdown('### See these variables by NPA')
        variableToView = st.selectbox(label="Variable",options=clusteringFields,key=0,format_func=lambda x: x.replace('_', ' '))
        from sklearn.preprocessing import minmax_scale
        dataForMap = master[['NPA',variableToView]]
        dataForMap = pd.merge(dataForMap,df2[['NPA','coordinates']],on="NPA",how="left")
        dataScaled = minmax_scale(dataForMap[variableToView].to_frame(),axis=0)
        dataScaled = pd.DataFrame(dataScaled)
        dataForMap['scaled'] = dataScaled

        dataForMap['fill_color'] = dataForMap['scaled'].apply(lambda x: [26,136,32,x*200])
        dataForMap['tooltip_text'] = dataForMap[variableToView].apply(lambda x: '{}: {}'.format(variableToView.replace('_',' '),x))
        # st.write(dataForMap)

        variable_layer = pdk.Layer(
            'PolygonLayer',
            data=dataForMap,
            filled=True,
            extruded=False,
            get_fill_color="fill_color",
            get_polygon="coordinates",
            get_line_color=[0,0,0],
            lineWidthMinPixels=1,
            pickable=True,
            auto_highlight=True
        )

        tooltip2 = {
            "html": "<b>NPA: {NPA}</b><br><b>{tooltip_text}"
        }

        deck2 = pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            layers=[variable_layer,road_layer],
            initial_view_state=view_state,
            tooltip=tooltip2
        )
        st.pydeck_chart(deck2)


if __name__ == "__main__":
    run()
