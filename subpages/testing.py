# -*- coding: utf-8 -*-
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as comps
import geopandas as gpd
from PIL import Image
import json
import pydeck as pdk
from pydeck.types import String
def run():
    st.title('Visuals')
    st.write("Visuals along Beatties Ford Road from North to South")

    jsonData = json.load(open('./qol-data/npa.json'))
    frame = pd.DataFrame()
    frame['coordinates']= [feature['geometry']['coordinates'] for feature in jsonData['features']]
    frame['NPA']= [int(feature['properties']['id']) for feature in jsonData['features']]
    
    master = pd.read_pickle('./qol-data/master.pkl')
    
    forMap = pd.merge(master[['NPA']],frame,how="left",on="NPA")

    npa_layer = pdk.Layer(
        'PolygonLayer',
        data=forMap,
        get_polygon='coordinates',
        filled=True,
        stroked=True,
        extruded=False,
        get_fill_color=[0,0,0,0],
        get_line_color=[0,0,0],
        lineWidthMinPixels=1,
        pickable=True,
        auto_highlight=True
    )
    
    labels = pd.read_csv('./qol-data/NPA_Labels.csv')
    labels['NPA_str'] = labels['NPA_str'].astype(str)
    
    label_layer = pdk.Layer(
        'TextLayer',
        data=labels,
        pickable=False,
        get_size=16,
        get_color=[1,1,1],
        get_position=['longitude','latitude'],
        get_text="NPA_str",
        get_angle=0,
        get_text_anchor=String("middle"),
        get_alignment_baseline=String("center")
    )
    
    view_state = pdk.ViewState(
        **{'latitude': 35.33, 'longitude': -80.89, 'zoom':10.50, 'maxZoom': 22, 'pitch': 0, 'bearing': 0})
    
    tooltip = {'html':'<b>NPA:</b> {NPA}'}
    
    deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        layers=[npa_layer,label_layer],
        initial_view_state=view_state,
        tooltip=tooltip)
    st.pydeck_chart(deck)
        
    
    st.image(Image.open('images/1house.png'))

    st.image(Image.open('images/2school.png'))

    st.image(Image.open('images/3school.png'))

    st.image(Image.open('images/4house.png'))

    st.image(Image.open('images/5house.png'))

    st.image(Image.open('images/6house.png'))

    st.image(Image.open('images/7house.png'))

    st.image(Image.open('images/9store.jpg'))

    st.image(Image.open('images/10house.png'))

    st.image(Image.open('images/11house.png'))
    
    st.image(Image.open('images/12mem.jpg'))
    
    st.image(Image.open('images/13house.png'))
    
    st.image(Image.open('images/14brew.png'))
    
    st.image(Image.open('images/15brew.png'))
    
    st.image(Image.open('images/16brew.png'))
    
    
if __name__ == '__main__':
    run()