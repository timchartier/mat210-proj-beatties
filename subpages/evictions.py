from numpy.core.records import fromfile
from numpy.core.shape_base import block
import streamlit as st
import pandas as pd
import pydeck as pdk
import json

def run():

    df = pd.read_csv('./eviction-lab-data/block-groups.csv')
    df = df[df['parent-location'] == "Mecklenburg County, North Carolina"]
    st.write(df.dtypes)

    # geojson = json.load(open('./eviction-lab-data/block-groups.geojson'))
    # geojson['features'] = [bg for bg in geojson['features'] if "Mecklenburg" in bg['properties']['pl']]
    # geoFrame = pd.DataFrame(geojson['features'])
    # geoFrame = pd.concat([geoFrame.properties.apply(pd.Series),geoFrame.geometry.apply(pd.Series)],axis=1)

    # st.write(geoFrame.dtypes)
    # geoFrame['coordinates'] = geoFrame['coordinates'].apply(lambda x: x[0])
    # st.write(geoFrame['coordinates'])

    # geo = pd.DataFrame()
    # geo['GEOID'] = [feature['properties']['GEOID'] for feature in geojson['features']]
    # geo['coordinates'] = [feature['geometry']['coordinates'][0] for feature in geojson['features']]

    beattiesGeoJson = "https://raw.githubusercontent.com/wesmith4/mat210-proj-beatties/main/beatties.geojson"
    # geo = pd.read_csv('./eviction-lab-data/meckBlockGroups.csv')
    # geo['GEOID'] = geo['GEOID'].astype(str)
    # combined = pd.merge(df,geo,on="GEOID",how="left")
    # geo.to_csv('./eviction-lab-data/meckBlockGroups.csv',index=False)

    geo = pd.read_csv('./eviction-lab-data/meckBlockGroups.csv')
    geo['coordinates'] = geo['coordinates'].apply(lambda x: eval(x))

    block_group_layer = pdk.Layer(
        'PolygonLayer',
        data=geo,
        filled=True,
        stroked=True,
        pickable=True,
        get_polygon="coordinates",
        lineWidthMinPixels=1,
        get_line_color=[0,0,0],
        get_fill_color=[0,0,0,0],
        extruded=False,
        auto_highlight=True
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

    tooltip = {
        "html": "<b>GEOID: {GEOID}</b>"
    }

    view_state = pdk.ViewState(
        **{"latitude": 35.33, "longitude": -80.89, "zoom": 10.50, "maxZoom": 22, "pitch": 0, "bearing": 0}
    )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
        initial_view_state=view_state,
        layers=[block_group_layer,road_layer],
        tooltip=tooltip
    )
    st.pydeck_chart(deck)