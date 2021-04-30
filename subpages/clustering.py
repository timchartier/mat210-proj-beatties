# Module imports
from sklearn.utils.validation import column_or_1d
import streamlit as st
# import plotly.express as px
# import plotly.figure_factory as ff
# import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
import json
import os
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import math
from . import mapping

def run():
    with st.beta_container():
        st.title('Clusters of neighborhoods along Beatties Ford Road')
    st.markdown("""

    In this project, we use an export from the Charlotte-Mecklenburg Quality of Life Explorer (QOL) as our primary dataset for the mathematical analyses and visualizations in the dashboard. This online tool, available at https://mcmap.org/qol/, is an excellent asset on its own, enabling comparison of its large selection of variables over the map of Mecklenburg County. The QOL Explorer divides Mecklenburg County into NPAs, or Neighborhood Profile Areas, for its spatial visualization of the included variables. As defined on the Explorer’s site:
    > *Neighborhood Profile Areas (NPAs) are geographic areas used for the organization and presentation of data in the Quality of Life Study.
    The boundaries were developed with community input and are based on one or more Census block groups.* (QOL)

    In our use of this data, we narrow the scope to the Neighborhood Profile Areas surrounding Beatties Ford Road, which we separate into "clusters" based on a mathematical method known as [*k-means clustering*](https://towardsdatascience.com/understanding-k-means-clustering-in-machine-learning-6a6e67336aa1), using curated sets of characteristics or characteristics of your choosing. Interpreting the clusters as presented in the map and data frame below, we assert that NPAs in the **same cluster** share **similar characteristics**, while NPAs in **different clusters** have **dissimilar characteristics**.

    Try clustering the NPAs according to the presets available in the dropdown list, but also experiment with your own selection of variables! Observing how certain clusterings are similar or different can provide exceptional insight into correlations between demographic, economic, educational, and many other kinds of factors.
    """)

    # Read in master data frame from pickle file
    master = pd.read_pickle('./qol-data/master.pkl')
    # Read in variable metadata from csv file
    metadata = pd.read_csv('./qol-data/csvFiles/metadata.csv')

    # Read in metadata lookup file
    variableLookup = pd.read_csv('./qol-data/variableLookup.csv')

    def formatChoice(x): return x.replace('_', ' ')

    # st.markdown('## Dynamic Chart')
    # variable = st.selectbox(label="Pick a variable", options=list(
    #     master.columns), format_func=lambda x: x.replace('_', ' '), index=5)
    # varCode = variableLookup[variableLookup['name'] == variable]['code'].values[0]
    # description = metadata[metadata['Short _Name'] == varCode]['Long_Description'].values[0]
    # st.write(description)

    # # st.write(master[variable])

    # fig2 = px.bar(master, x=variable, y="order", orientation="h",
    #               labels=dict(variable=formatChoice(variable), order="NPA"))
    # fig2.update_yaxes(autorange="reversed",
    #                   ticktext=master.NPA.tolist(), tickvals=master.order.to_list())
    # st.plotly_chart(fig2)


    # Section on clustering
    st.markdown("## Clustering NPAs")
    usableData = master.dropna(axis='columns').drop(columns=['NPA', 'order'])

    data = master[list(usableData.columns)].dropna(axis='columns')

    variablePresets = {
        'None': ['Population_Density_2018'],
        'Racial Composition': ["White_Population_2017","Black_Population_2017","Asian_Population_2017","Hispanic_Latino_2017","All_Other_Races_2017"],
        'Income, Economic': ['Household_Income_2018', 'Public_Nutrition_Assistance_2018','Employment_Rate_2017'],
        'Education': ['Proficiency_Elementary_School_2017','Proficiency_Middle_School_2017','High_School_Diploma_2017','Bachelors_Degree_2017', 'Early_Care_Proximity_2017'],
        'Health Resources Proximity':['Low_Cost_Healthcare_Proximity_2018','Pharmacy_Proximity_2018','Grocery_Proximity_2018'],
        'Transportation': ['Long_Commute_2018','Bicycle_Friendliness_2018','Street_Connectivity_2018','Sidewalk_Availability_2015','Transit_Proximity_2018'],
        'Engagement':['Arts_Participation_2013','311_Requests_2016','Voter_Participation_2018',],
        'Environment':['Tree_Canopy_2012','Residential_Tree_Canopy_2012','Impervious_Surface_2018','Natural_Gas_Consumption_2013','Water_Consumption_2018','Commuters_Driving_Alone_2018',],
        'Housing':['Housing_Density_2019','Single_Family_Housing_2019','Housing_Size_2019','Housing_Age_2019','Rental_Houses_2018','New_Residential_2018','Residential_Renovation_2018','Home_Sales_Price_2015','Home_Ownership_2018','Residential_Occupancy_2018',],
        'Crime':['Violent_Crime_Rate_2018','Property_Crime_Rate_2018','Disorder_Call_Rate_2018',]
    }

    with st.beta_container():
        # Streamlit multiselect to pick fields for clustering; => Default ["White_Population_2020"]
        col1, col2 = st.beta_columns((4, 2))

        with col1:
            whichPreset = st.selectbox(
                label="Use curated presets of variables",
                options=list(variablePresets.keys()),
                index=1
            )
        clusteringFields = st.multiselect(label='Or, select specific fields for clustering (or modify the presets!)',
                                            options=list(usableData.drop(columns=['Area','Area.1']).columns),
                                            format_func=lambda x: x.replace(
                                                '_', ' '),
                                            default=variablePresets[whichPreset],
                                            help="Choose from the dropdown, or type to search.")
        with st.beta_expander("Variable Descriptions",expanded=len(clusteringFields) > 0):
            for var in clusteringFields:
                varCode = variableLookup[variableLookup['name'] == var]['code'].values[0]
                description = metadata[metadata['Short _Name'] == varCode]['Long_Description'].values[0]
                st.markdown("""
                - `{}`: {}
                """.format(var, description))
        st.empty()

    numberOfClusters = col2.number_input(
        label="Number of Clusters", min_value=2, max_value=5, value=2,help="Min: 2, Max: 5")

    # If no fields selected, give error
    if len(clusteringFields) == 0:
        st.text("")
        st.error("Please select one or more fields for clustering NPAs.")
    # Else display the clusters and map
    else:

        selectedData = data[clusteringFields]
        scaled = normalize(selectedData, axis=0)
        scaled = pd.DataFrame(scaled, columns=selectedData.columns)

        # st.write(selectedData)

        kmeansClusters = KMeans(n_clusters=numberOfClusters, random_state=42)
        kmeansClusters.fit(scaled)

        master['cluster'] = kmeansClusters.labels_ + 1
        master['cluster'] = master['cluster'].astype(int)

        df2 = pd.DataFrame()

        palette = [
            [255, 75, 75, 100],
            [255, 191, 0, 100],
            [47, 114, 255, 100],
            [64, 255, 112, 100],
            [186, 73, 255, 100]
        ]

        def getClusterColor(x): return palette[x]

        def getColor(x):
            if math.isnan(x):
                return [0, 0, 0, 0]
            else:
                return palette[int(x-1)]

        # json = pd.read_json('./qol-data/npa.json')
        jsonData = json.load(open('./qol-data/npa.json'))

        df2['coordinates'] = [feature['geometry']['coordinates']
                              for feature in jsonData['features']]
        df2['NPA'] = [int(feature['properties']['id'])
                      for feature in jsonData['features']]
        df2 = pd.merge(df2, master[["NPA", "cluster"]], on="NPA", how="left")
        df2['fill_color'] = df2['cluster'].map(getColor)
        df2['cluster_tooltip'] = df2['cluster'].map(
            lambda x: 'Cluster {}'.format(int(x)) if x > 0 else '')
        df2 = df2.drop(columns=['cluster'])

        # Summary of data by cluster
        st.markdown('### Variable averages by cluster')
        summary = master.groupby('cluster').mean()[clusteringFields]
        summary['Cluster'] = summary.index.map(
            lambda x: 'Cluster {}'.format(x))
        summary = summary[['Cluster'] + clusteringFields]

        def getSummaryColor(row):
            ind = int(row.Cluster.split(' ')[1]) - 1
            colorCode = palette[ind]
            return ['background-color: rgba({},{},{},.3)'.format(colorCode[0], colorCode[1], colorCode[2], colorCode[3])]*(1+len(clusteringFields))
        summary = summary.style.apply(getSummaryColor, axis=1)
        st.write(summary)

        # st.write(df2)


        polygon_layer = mapping.generateNPALayer(df2,variable_fill=True,variable_name="fill_color")

        road_layer = mapping.generateRoadLayer()

        tooltip = {"html": "<b>NPA:</b> {NPA} <br /><b>{cluster_tooltip}</b>"}

        deck = mapping.createDeck(layers=[polygon_layer,road_layer],showTooltip=True,tooltip=tooltip)

        descriptions = {
            'None': {
                'description': """Description for no preset selected"""
            },
            'Racial Composition': {
                'description': """
                    Considering this map, notice especially the great degree of polarity between the `White_Population_2017` and `Black_Population_2017` averages for the displayed clusters (these are percents of the total population). 
                    
                    When we construct 2 clusters of these NPAs, we observe quite a clean geographic break between a northern section and a southern section of the area along Beatties Ford Road, with large differences between these clusters' average racial composition. As we change this number to 3, 4, or 5 clusters, we identify smaller, more specific areas with even greater racial uniformity.

                    Additionally, try comparing the two-cluster map using these variables with the two-cluster map using the variables for "Household Income 2017" and "Home Sales Price 2015." The similarity is quite striking.
                """
            },
            'Income, Economic': {
                'description': """
                    It is apparent with these clusterings that residents of the NPAs farther north experience greater degrees economic privilege than those closer to downtown Charlotte. 

                    When we use two clusters, we see a north-south split similar to that observed in the clustering according to racial composition. When observing how the NPAs are separated into 5 clusters, we notice that the `Household_Income_2018` variable quite obviously declines in progression from north to south along the road.

                    You will notice in various clusterings that the pair of NPAs 421 and 447 consistently appear in the most privileged clusters.
                """
            },
            'Education': {
                'description': """
                    The clustering of the NPAs along the road based on these education variables turns out remarkably similar to that produced in the clustering for racial composition. For example, notice that the construction of two clusters based on educational variables appears nearly the same as the two clusters based on racial composition, where the cluster with averages indicating lower academic proficiency or success correlates with the cluster with a higher average percentage of black residents.

                    Interestingly, increasing the number of clusters here (try 4 or 5) reveals that a hypothetical "academic index" based on the cluster averages for these variables would clearly decrease from north to south along the road.

                    We should note that the Early Care Proximity variable in this set shows the highest values in the cluster(s) closer to downtown Charlotte. This likely is due to the proximity to an urban area in addition to other demographic factors.
                """
            },
            'Health Resources Proximity': {
                'description':"""
                    This set of variables does not yield clusters as "clean" or informative as in some of the other sets. 
                    
                    This is likely due to the fact that the values of these "proximity" variables may be determined in one part by a collection of demographic/economic factors as we have discussed, and in another part by the NPA's proximity to the urban center of Charlotte, where a greater concentration of resources is to be expected.
                """
            },
            'Transportation': {
                'description': """
                    Observing the clusters produced by this set, we may assert that the proximity to Charlotte's downtown has the most impact on the values for these variables.

                    These clusters do provide valuable insight to the transportation-related structures and resources available to residents in these NPAs - for example, those living in Cluster 1 according to the 3-cluster map have great access to public transit, and benefit from relative ease of navigating their areas on foot compared to the other clusters.
                """
            },
            'Engagement': {
                'description': """
                    From these clustering results, the biggest takeaways are the relatively higher participation in arts and culture activities by the residents of the clusters farther north on the map compared to the clusters closer to downtown, as well as these clusters' relatively higher voter participation rates. 
                    
                    These statistics may be indicators of greater connectivity in these clusters' communities or greater agency or availability of disposable time to participate in such activities.

                """
            },
            'Environment': {
                'description': """
                    The learnings from this clustering largely may be observed with a glance at the satellite map of the area (take a look at the Annotated Google Map) – as expected when comparing urban areas with suburban or rural areas, the clusters closer to downtown show a lesser extent of tree canopy than the clusters farther north

                    Logically, these clusters closer to urban Charlotte also have higher average values for the percent of land area classified as "impervious surface," as indicated by the `Impervious_Surface_2018` variable.
                """
            },
            'Housing': {
                'description': """
                    Observing the division of NPAs into clusters according to these variables provides insight into the different kinds of residential circumstances that are present in each area. In this case, using 4 or 5 clusters gives more interpretable visualization.

                    Regarding spatial and aesthetic variables, we can observe that clusters near the downtown area have much greater density of housing units in their land area than do the clusters farther north along the road, and in general these housing units are smaller. This is consistent with expectations for urban density compared with surrounding suburbs and more rural areas.

                    We also find that residents in the NPAs in the clusters closer to Huntersville own their homes at a greater rate relative to other clusters, and these homes are more valuable (as measured by average Home Sales Price).
                """
            },
            'Crime': {
                'description': """
                    Observing these clusterings acccording to crime-related variables, we can discern that the common assumption of a greater magnitude of crime occurring as one nears an urban area holds true in this case, with some degree of nuance. Regardless of the number of clusters used here, there is a large cluster of NPAs in the northern section that has significant lower average crime rates than the rest of the clusters. 

                    Interestingly, we observe that the NPAs right at the end of Beatties Ford road, around Johnson C. Smith University show lower rates of crime than those just to the north, which goes against the mentioned assumption. When creating 5 clusters for these variables, we can see that the two clusters with the highest property and violent crime rates are single NPAs – 70 and 374 – which include West Charlotte High School and Lincoln Heights Neighborhood Park, respectively.

                """
            }
        }


        # If selected fields are same as one of the presets, show our explanatory text with the map.
        st.write('### Cluster Map')
        # sortedClusteringFields = clusteringFields.sort()
        if clusteringFields.copy().sort() == variablePresets[whichPreset].copy().sort()\
            and len(clusteringFields) == len(variablePresets[whichPreset])\
            and not whichPreset == 'None'\
            and not descriptions[whichPreset]['description'] == '': # don't leave space for missing descriptions

            colA,colB,colC = st.beta_columns([10,1,9])
            with colA:
                st.pydeck_chart(deck)
            with colC:
                st.write(descriptions[whichPreset]['description'])
        # Otherwise, just show the map
        else:
            colA,colB,colC = st.beta_columns([2,4,2])
            with colB:
                st.pydeck_chart(deck)

        # View single variable on NPA map
        colX,colY,colZ = st.beta_columns([2,4,2])
        with colY:
            st.markdown('### Visualize these variables individually by NPA')
            variableToView = st.selectbox(label="Variable",options=clusteringFields,key=0,format_func=lambda x: x.replace('_', ' '))
            from sklearn.preprocessing import minmax_scale
            dataForMap = master[['NPA',variableToView]]
            dataForMap = pd.merge(dataForMap,df2[['NPA','coordinates']],on="NPA",how="left")
            dataScaled = minmax_scale(dataForMap[variableToView].to_frame(),axis=0)
            dataScaled = pd.DataFrame(dataScaled)
            dataForMap['scaled'] = dataScaled

            dataForMap['fill_color'] = dataForMap['scaled'].apply(lambda x: [26,136,32,x*200])
            dataForMap['tooltip_text'] = dataForMap[variableToView].apply(lambda x: '{}: {}'.format(variableToView.replace('_',' '),x))
            # dataForMap['label_coordinates'] = dataForMap['coordinates'].apply(lambda x: [sum(y)/len(y) for y in zip(*x[0])])
            # NPA_Labels = dataForMap.loc[:,['NPA','label_coordinates']]
            # NPA_Labels.loc[:,'NPA_str'] = NPA_Labels.loc[:,'NPA'].apply(lambda x: str(x))
            # NPA_Labels[['longitude','latitude']] = pd.DataFrame(NPA_Labels.label_coordinates.to_list(),index=NPA_Labels.index)
            # NPA_Labels = NPA_Labels.drop(columns=['label_coordinates'])
            # NPA_Labels.to_csv('./qol-data/NPA_Labels.csv',index=False)

            NPA_Labels = pd.read_csv('./qol-data/NPA_Labels.csv')

            variable_layer = mapping.generateNPALayer(dataForMap)

            npa_label_layer = mapping.generateNPALabelsLayer(NPA_Labels)

            tooltip2 = {
                "html": "<b>NPA: {NPA}</b><br><b>{tooltip_text}"
            }

            deck2 = mapping.createDeck(layers=[variable_layer,npa_label_layer,road_layer],tooltip=tooltip2)
            st.pydeck_chart(deck2)
            st.write("""
            In this map above, greater opacities of the shading of NPAs signify greater values for the selected `{}` variable.
            """.format(variableToView))


if __name__ == "__main__":
    run()
