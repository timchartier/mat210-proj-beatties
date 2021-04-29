import pydeck as pdk
from pydeck.types import String
import streamlit as st

# @st.cache
def generateNPALayer(data_frame, variable_fill=True,variable_name="fill_color",uniform_fill=[0,0,0,0],pickable=True):
    """
    Arguments:

        data_frame: which data frame are you trying to map?

        variable_fill: Use variable in data for fill colors? (True/False)

        variable_name: If so, which variable? (Default = "fill_color")

        uniform_fill: If uniform fill, a list for rgba (e.g. [0,0,0,0] for transparent)

        pickable: do you want this layer to be pickable? (True/False)


    """
    return pdk.Layer(
        'PolygonLayer',
        data=data_frame,
        filled=True,
        extruded=False,
        stroked=True,
        get_fill_color=variable_name if variable_fill else uniform_fill,
        get_polygon="coordinates",
        get_line_color=[0,0,0],
        lineWidthMinPixels=1,
        pickable=pickable,
        auto_highlight=True
    )

# @st.cache
def generateNPALabelsLayer(label_file):
    """
        Generates Layer for NPA number labels at the average lng-lat for each NPA.

        label_file: dataframe with columns "NPA_str", "longitude", and "latitude"
    """
    label_file["NPA_str"] = label_file["NPA_str"].astype(str)

    return pdk.Layer(
        'TextLayer',
        data=label_file,
        pickable=False,
        get_size=16,
        get_color=[1,1,1],
        get_position=['longitude','latitude'],
        get_text="NPA_str",
        get_angle=0,
        get_text_anchor=String("middle"),
        get_alignment_baseline=String("center")
    )

# @st.cache
def generateRoadLayer():
    """
        No arguments here. Just generates layer for Beatties Ford Road highlighted in Blue.
    """
    beattiesGeoJson = "https://raw.githubusercontent.com/wesmith4/mat210-proj-beatties/main/beatties.geojson"
    return pdk.Layer(
        'GeoJsonLayer',
        data=beattiesGeoJson,
        filled=True,
        pickable=False,
        lineWidthMinPixels=3,
        get_line_color=[0,0,200],
        opacity=1,
        use_binary_transport=False,
        extruded=True
    )

defaultTooltip = {"html": "<b>NPA:</b> {NPA}"}
# @st.cache
def createDeck(layers,showTooltip=True,tooltip=defaultTooltip):
    """
    Creates the "Deck" object to be passed into st.pydeck_chart()

    Arguments
    ------------
    layers: list of layers to include in the deck

    showTooltip: whether to show a tooltip (True/False). This should correspond to some layer that is pickable.

    tooltip: custom tooltip object. E.g. `{"html": "<b>NPA:</b> {NPA}<br><b>YOUR_VARIABLE_NAME:</b> {COLUMN_NAME}"}`
    """
    view_state = pdk.ViewState(
            **{"latitude": 35.33, "longitude": -80.89, "zoom": 10.50, "maxZoom": 22, "pitch": 0, "bearing": 0}
        )
    return pdk.Deck(
        layers=layers,
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=view_state,
        tooltip=tooltip
    )
