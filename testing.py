import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt

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