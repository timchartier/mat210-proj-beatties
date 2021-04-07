import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
import pydeck as pdk
import geopandas as gpd

import streamlit.components.v1 as components

st.title('Beatties Ford Road Project')


st.video('https://www.youtube.com/watch?v=sK-MlWm7Iuc')


grocery = pd.read_csv('./grocery-data/Grocery_Stores.csv')
grocery = grocery.rename(columns={'X': 'longitude', 'Y': 'latitude'})

colNames = grocery.columns

st.write("Hello world")
st.write(colNames)

coords = grocery[['longitude', 'latitude']]
avgLong = grocery['longitude'].median()
avgLat = grocery['latitude'].median()

beattiesGeoJson = "https://raw.githubusercontent.com/wesmith4/mat210-proj-beatties/main/beatties.geojson"

st.write("""## Grocery stores in Mecklenburg County""")
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=35.285122,
         longitude=-80.846734,
         zoom=9.5,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=coords,
             get_position=['longitude','latitude'],
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
         pdk.Layer(
             'GeoJsonLayer',
             data=beattiesGeoJson,
             filled=True,
             pickable=True,
             lineWidthMinPixels=2,
             opacity=1,
             id='beatties-ford-road',
             use_binary_transport=False
         )

     ],
))

components.html("""
<iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.socialexplorer.com/bc9c206f28/embed" width="640" height="480" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
""", width=640,height=480)

components.html("""
    <iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.socialexplorer.com/7e100dcc9b/embed" width="640" height="480" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
""", width=640,height=480)


