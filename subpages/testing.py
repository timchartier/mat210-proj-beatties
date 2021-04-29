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
from . import mapping
def run():
    st.title('A Journey Down Beatties Ford Road')
    st.write('**Sights along Beatties Ford Road from North to South**')
    st.write('\n')
    st.write('As Beatties Ford runs from Huntersville to West Charlotte, the sights along the way are not uniform. Housing quality, racial demographics of neighborhoods, and the prevalence of fast food chains begin to shift as the road travels south. Before using the data collected on various socioeconomic indicators for different areas along the road and in different time periods, let us first journey down the road and examine the sights that are seen on the way.')
    st.write('The Quality of Life Explorer divides Mecklenburg County into NPAs, or Neighborhood Profile Areas, for its spatial visualization of the included variables.')
    st.markdown("""
    
    As defined by the [Quality of Life Study](https://mcmap.org/qol/#15/):

    > *Neighborhood Profile Areas (NPAs) are geographic areas used for the organization and presentation of data in the Quality of Life Study.
    The boundaries were developed with community input and are based on one or more Census block groups.*

    """)
    st.write('\n')
    st.write('As we visualize a drive down Beatties Ford Road, different sights will be marked by which NPA they are in, and will be ordered from north to south. Not all locations will be directly on Beatties Ford Road, but in the same NPA or nearby. The NPAs that Beatties Ford Road runs through are shown in the map below:')
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

    road_layer = mapping.generateRoadLayer()
    
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
        layers=[npa_layer,label_layer,road_layer],
        initial_view_state=view_state,
        tooltip=tooltip)
    st.pydeck_chart(deck)
    
    st.write('')
    st.write('')
    
    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(Image.open('images/1house.png'))
    with col2:
        st.write('**NPA 450**')
        st.write(' ')
        st.write('House on Savannah Grace Lane.')
       
        
    col3, col4 = st.beta_columns(2)
    with col4:
        st.image(Image.open('images/2school.png'))
    with col3:
        st.write('**NPA 450**')
        st.write(' ')
        st.write('Front of Francis Bradley Middle School.') 
    col5, col6 = st.beta_columns(2)
    with col5:
        st.image(Image.open('images/3school.png'))
    with col6:
        st.write('**NPA 447**')
        st.write(' ')
        st.write('View of Community School of Davidson.')

    col7, col8 = st.beta_columns(2)
    with col8:
        st.image(Image.open('images/4house.png'))
    with col7:
        st.write('**NPA 447**')
        st.write(' ')
        st.write('House along Carrington Ridge Drive.')

    col9, col10 = st.beta_columns(2)
    with col9:  
        st.image(Image.open('images/5house.png'))
    with col10:
        st.write('**NPA 447**')
        st.write(' ')
        st.write('House along Mclothian Lane.')

    col11, col12 = st.beta_columns(2)
    with col12:
        st.image(Image.open('images/6house.png'))
    with col11:
        st.write('**NPA 209**')
        st.write(' ')
        st.write('Streetview of Davis Meadows Drive.')
        
    col13, col14 = st.beta_columns(2)
    with col13:     
        st.image(Image.open('images/7house.png'))
    with col14:
        st.write('**NPA 280**')
        st.write(' ')
        st.write('Streetview of Countrywoods Mobile Home Park. The number of mobile homes increases as we travel more south; the particular park is in NPA 280, southeast of NPA 209.')

    col15, col16 = st.beta_columns(2)
    with col16:
        st.image(Image.open('images/9store.jpg'))
    with col15:
        st.write('**NPA 123**')
        st.write(' ')
        st.write("Storefront of Firestone-Garden Park. The number of fast food restaurants such as Little Caesar's is also increasing.")
    
    col17, col18 = st.beta_columns(2)
    with col17:
        st.image(Image.open('images/10house.png'))
    with col18:
        st.write('**NPA 385**')
        st.write(' ')
        st.write('Streetview of Charlotte Village Mobile Home. Another trailer park in the area, NPA 385 is southwest of NPA 123.')
    
    col19, col20 = st.beta_columns(2)
    with col20:
        st.image(Image.open('images/11house.png'))
    with col19:
        st.write('**NPA 374**')
        st.write(' ')
        st.write('Lincoln Heights made headlines in June 2020 after a shooting occurred in the area.')
    
    col21, col22 = st.beta_columns(2)
    with col21:
        st.image(Image.open('images/12mem.jpg'))
    with col22:
        st.write('**NPA 374**')
        st.write(' ')
        st.write('A memorial for the victims of the June 22nd, 2020 shooting. The incident occurred near the intersection of Beatties Ford Road and Catherine Simmons Avenue.')
    
    col23, col24 = st.beta_columns(2)
    with col24:
        st.image(Image.open('images/13house.png'))
    with col23:
        st.write('**NPA 85**')
        st.write(' ')
        st.write('Washington Heights is one of the neighborhoods int he area with a historic past. It was made as a neighborhood for the rising Black middle-class in the early 20th century.')
    
    col25, col26 = st.beta_columns(2)
    with col25:
        st.image(Image.open('images/14brew.png'))
    with col26:
        st.write('**NPA 347**')
        st.write(' ')
        st.write("Blue Blaze Brewery. Now that we're closer to Charlotte, note the difference in surrounding restaurants.")
    col27, col28 = st.beta_columns(2)
    
    with col28:
        st.image(Image.open('images/16brew.png'))
    with col27:
        st.write('**NPA 340**')
        st.write(' ')
        st.write('VBGB Beer Hall and Garden.')
    
    col29, col30 = st.beta_columns(2)
    with col29:
        st.image(Image.open('images/15brew.png'))
    with col30:
        st.write('**NPA 340**')
        st.write(' ')
        st.write('Storefront of VBGB Beer Hall and Garden - now, at the end of Beatties Ford Road, the surrounding area is starting to look like how much of West Charlotte does.')
    
    
    
if __name__ == '__main__':
    run()