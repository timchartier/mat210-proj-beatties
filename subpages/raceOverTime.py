import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


def run():

    DATA_FILE = os.path.join(os.path.dirname(__file__),'master.pkl')

    col1,col2,col3 = st.beta_columns([1,1,1])

    master = pd.read_pickle('./qol-data/master.pkl')
    master.columns = master.columns.str.replace(' ','')
    # Construct dataframe for population by race

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

    col1.plotly_chart(graphs['2000'],use_container_width=True)
    col2.plotly_chart(graphs['2010'],use_container_width=True)
    col3.plotly_chart(graphs['2018'],use_container_width=True)


if __name__ == "__main__":
    run()