import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
import pydeck as pdk

import streamlit.components.v1 as components

st.title('My first Streamlit app')

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

myArray = np.array([[1,2,3],[4,5,6]])
myArray

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['a','b','c']
)

st.area_chart(chart_data)

# Chart data here
chart_data

st.video('https://www.youtube.com/watch?v=sK-MlWm7Iuc')


"""
# This is a markdown header
Some markdown text here.

"""

grocery = pd.read_csv('./grocery-data/Grocery_Stores.csv')
grocery = grocery.rename(columns={'X': 'longitude', 'Y': 'latitude'})

colNames = grocery.columns

st.write("Hello world")
st.write(colNames)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=grocery,
             get_position=['longitude','latitude'],
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
))

st.write("trying again")

