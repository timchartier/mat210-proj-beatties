import streamlit as st

# Import subpages
import subpages.home as home
import subpages.clustering as clustering
import subpages.beatties as beatties
import subpages.evictions as evictions
import subpages.testing as journey
import subpages.quick_history as history
import subpages.googleMap as googleMap
import subpages.references as references
# This is the master file for the Beatties Ford Road dashboard
st.set_page_config(page_title="Beatties Ford Road", layout="wide")

# Set up sidebar for navigation
PAGES = {
    # dict of pages here
    'Home': home,
    'Journey down Beatties Ford Road': journey,
    'Clusters of neighborhoods': clustering,
    # 'Beatties': beatties,
    'Beatties Ford Road over time' : history,
    # 'Demographics over Time': raceOverTime,
    # 'Evictions': evictions,
    "Annotated Google Map": googleMap,
    "References": references
}
st.sidebar.markdown('## Page Navigation')
selectedPage = st.sidebar.radio(
    "Navigate to:", options=list(PAGES.keys()), index=0)

subApp = PAGES[selectedPage]
subApp.run()
