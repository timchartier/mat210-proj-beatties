import streamlit as st

# Import subpages
import subpages.home as home
import subpages.clustering as clustering
import subpages.beatties as beatties
import subpages.raceOverTime as raceOverTime

# This is the master file for the Beatties Ford Road dashboard
st.set_page_config(page_title="Beatties Ford Road", layout="wide")

# Set up sidebar for navigation
PAGES = {
    # dict of pages here
    'Home': home,
    'Clustering': clustering,
    'Beatties': beatties,
    'Demographics over Time': raceOverTime
}
st.sidebar.markdown('## Page Navigation')
selectedPage = st.sidebar.radio(
    "Navigate to:", options=list(PAGES.keys()), index=0)

subApp = PAGES[selectedPage]
subApp.run()
