import streamlit as st
import pandas as pd
import json
import mapping

def run():

    df = pd.read_csv('./eviction-lab-data/block-groups.csv')
    df = df[df['parent-location'] == "Mecklenburg County, North Carolina"]
    # st.write(df.dtypes)
    st.write(df)

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

    # # geo = pd.read_csv('./eviction-lab-data/meckBlockGroups.csv')
    # # geo['GEOID'] = geo['GEOID'].astype(str)
    # # combined = pd.merge(df,geo,on="GEOID",how="left")
    # # geo.to_pickle('./eviction-lab-data/meckBlockGroups.pkl')
    # geo.to_csv('./eviction-lab-data/meckBlockGroups.csv',index=False)

    # geo = pd.read_pickle('./eviction-lab-data/meckBlockGroups.pkl')
    geo = pd.read_csv('./eviction-lab-data/meckBlockGroups.csv')
    geo['GEOID'] = geo['GEOID'].astype(str)
    geo.loc[:,'coordinates'] = geo.loc[:,'coordinates'].apply(lambda x: eval(x))

    block_group_layer = mapping.generateNPALayer(geo,variable_fill=False)

    road_layer = mapping.generateRoadLayer()

    tooltip = {
        "html": "<b>GEOID: {GEOID}</b>"
    }

    deck = mapping.createDeck(layers=[block_group_layer,road_layer],tooltip=tooltip)
    st.markdown('## Block group map')
    st.pydeck_chart(deck)