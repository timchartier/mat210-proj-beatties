# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:32:40 2021

@author: liamc
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os


def run():
    
    with st.beta_container():
        st.title('Looking at the data over time')
    st.markdown("""
    This page takes a look through at four selected variables spanning over time.
    "In these charts below, note that the NPAs are ordered to roughly mirror their geographical positions from north to south along Beatties Ford Road."
    """)

    DATA_FILE = os.path.join(os.path.dirname(__file__),'../qol-data/master.pkl')

    # master = pd.read_pickle('./qol-data/master.pkl')
    master = pd.read_pickle(DATA_FILE)
    master.columns = master.columns.str.replace(' ','')
    # Construct dataframe for population by race

#sales price/value graphs
    #housing prices
    hp_graphs = {}
    for year in ['2013','2015']:
        data = master.loc[:,['NPA', 'order', 'Home_Sales_Price_{}'.format(year)]]
        data.columns = ['NPA', 'order', 'Home Sales Price']
        data.loc[:,['Home Sales Price']] = data[['Home Sales Price']].astype(float)

        melted = pd.melt(data, id_vars=['NPA', 'order'], value_vars=[
            'Home Sales Price'], value_name="price")

        fig = px.bar(melted, y="order", x="price",
                    orientation="h", labels=dict(order="NPA", price="Price"), title="Average Housing Prices by NPA ({})".format(year))
        fig.update_yaxes(autorange="reversed",
                        ticktext=data.NPA.tolist(), tickvals=data.order.to_list())
        fig.update_layout(legend=dict(
            yanchor="top",
            y=-.2,
            xanchor="left",
            x=0.01,
            orientation='h'
        ))

        hp_graphs[year] = fig
    st.markdown('## Housing Prices by NPA over time')
    hp_col1,hp_col2= st.beta_columns([1,1])
    hp_col1.plotly_chart(hp_graphs['2013'],use_container_width=True)
    hp_col2.plotly_chart(hp_graphs['2015'],use_container_width=True)

    with st.beta_container():  #INSERT ANALYSIS
        st.markdown("""
        FILL WITH ANALYSIS OF RESULTS
        """)
    #insert rental costs from 2017-2018???

#household income
    hi_graphs = {}
    for year in ['2017','2018']:
        data = master.loc[:,['NPA', 'order', 'Household_Income_{}'.format(year)]]
        data.columns = ['NPA', 'order', 'Household Income']
        data.loc[:,['Household Income']] = data[['Household Income']].astype(float)

        melted = pd.melt(data, id_vars=['NPA', 'order'], value_vars=[
            'Household Income'], value_name="hh_inc")

        fig = px.bar(melted, y="order", x="hh_inc", 
                    orientation="h", labels=dict(order="NPA", hh_inc="Household Income"), title="Average Household Income for {}".format(year))
        fig.update_yaxes(autorange="reversed",
                        ticktext=data.NPA.tolist(), tickvals=data.order.to_list())
        fig.update_layout(legend=dict(
            yanchor="top",
            y=-.2,
            xanchor="left",
            x=0.01,
            orientation='h'
        ))

        hi_graphs[year] = fig
    st.markdown('## Household Income over time')
    hi_col1,hi_col2 = st.beta_columns([1,1])
    hi_col1.plotly_chart(hi_graphs['2017'],use_container_width=True)
    hi_col2.plotly_chart(hi_graphs['2018'],use_container_width=True)

    with st.beta_container():
        st.markdown("""
        FILL WITH ANALYSIS OF RESULTS
        """)


#employment rate
    er_graphs = {}
    for year in ['2017','2018']:
        data = master.loc[:,['NPA', 'order', 'Employment_Rate_{}'.format(year)]]
        data.columns = ['NPA', 'order', 'Employment Rate']
        data.loc[:,['Employment Rate']] = data[['Employment Rate']].astype(float)

        melted = pd.melt(data, id_vars=['NPA', 'order'], value_vars=[
            'Employment Rate'], value_name="e_rate")

        fig = px.bar(melted, y="order", x="e_rate",
                    orientation="h", labels=dict(order="NPA", e_rate="Employment Rate"), title="Employment Rate for {}".format(year))
        fig.update_yaxes(autorange="reversed",
                        ticktext=data.NPA.tolist(), tickvals=data.order.to_list())
        fig.update_layout(legend=dict(
            yanchor="top",
            y=-.2,
            xanchor="left",
            x=0.01,
            orientation='h'
        ))

        er_graphs[year] = fig
    st.markdown('## Racial Breakdowns by NPA over time')
    st.markdown("In these charts below, note that the NPAs are ordered to roughly mirror their geographical positions from north to south along Beatties Ford Road.")
    er_col1,er_col2 = st.beta_columns([1,1])
    er_col1.plotly_chart(er_graphs['2017'],use_container_width=True)
    er_col2.plotly_chart(er_graphs['2018'],use_container_width=True)

    with st.beta_container():
        st.markdown("""
        FILL WITH ANALYSIS OF RESULTS
        """)


#racial graphs
    graphs = {}
    for year in ['2000','2010','2018']:
        data = master.loc[:,['NPA', 'order', 'Population_{}'.format(year), 'White_Population_{}'.format(year),
                    'Black_Population_{}'.format(year), 'Asian_Population_{}'.format(year), 'Hispanic_Latino_{}'.format(year), 'All_Other_Races_{}'.format(year)]]
        data.columns = ['NPA', 'order', 'Total Population',
                        'White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']
        data.loc[:,['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']
            ] = data[['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']].astype(float)
        data.loc[:,['White', 'Black', 'Asian', 'Hispanic/Latino', 'Other']] = data[['White', 'Black',
                                                                            'Asian', 'Hispanic/Latino', 'Other']].multiply(data['Total Population'], axis="index")/100

        melted = pd.melt(data, id_vars=['NPA', 'order'], value_vars=[
            'White', 'Black', 'Asian', 'Hispanic/Latino', 'Other'], var_name="Race", value_name="population")

        fig = px.bar(melted, y="order", x="population", color="Race",
                    orientation="h", labels=dict(order="NPA", population="Population"), title="Population by Race ({})".format(year))
        fig.update_yaxes(autorange="reversed",
                        ticktext=data.NPA.tolist(), tickvals=data.order.to_list())
        fig.update_layout(legend=dict(
            yanchor="top",
            y=-.2,
            xanchor="left",
            x=0.01,
            orientation='h'
        ))

        graphs[year] = fig
    st.markdown('## Racial Breakdowns by NPA over time')
    st.markdown("In these charts below, note that the NPAs are ordered to roughly mirror their geographical positions from north to south along Beatties Ford Road.")
    col1,col2,col3 = st.beta_columns([1,1,1])
    col1.plotly_chart(graphs['2000'],use_container_width=True)
    col2.plotly_chart(graphs['2010'],use_container_width=True)
    col3.plotly_chart(graphs['2018'],use_container_width=True)

    with st.beta_container():
        st.markdown("""
        FILL WITH ANALYSIS OF RESULTS
        """)

    

if __name__ == "__main__":
    run()