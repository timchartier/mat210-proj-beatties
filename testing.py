import pandas as pd
import numpy as np
import streamlit as st

import streamlit.components.v1 as components

st.title('My first Streamlit app')

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.map()