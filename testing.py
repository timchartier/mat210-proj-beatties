import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import os


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

df = getDataFrame(dataFrames['Economy'])
df[['Household_Income_2017','Household_Income_2018']] = df[['Household_Income_2017','Household_Income_2018']].astype(float)
master[['Household_Income_2017','Household_Income_2018']] = master[['Household_Income_2017','Household_Income_2018']].astype(float)



st.write(master)
