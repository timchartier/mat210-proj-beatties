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
def run():
    st.title('Visuals')
    st.write("Visuals along Beatties Ford Road from North to South")

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