import streamlit as st
import streamlit.components.v1 as comps
def run():

    st.sidebar.write("(Close this sidebar to view the whole map)")
    col1,col2,col3 = st.beta_columns([1,5,1])
    with col2:
        st.title("Annotated Google Map")


        st.markdown("""
        View our Google My Map with collections of fast food restaurants, schools, churches, and other locations along Beatties Ford Road. Open the sidebar with the icon at the top left of the map to select or deselect location layers.

        You can also view the full version of the map at [this link](https://www.google.com/maps/d/edit?mid=10yFAFu1L3DirUntm6-A3b7FOweTFr95b&usp=sharing).
        
        
        """)
        comps.html("""
            <iframe src="https://www.google.com/maps/d/u/0/embed?mid=10yFAFu1L3DirUntm6-A3b7FOweTFr95b&amp;z=13.8&ll=35.335%2C-80.885" width="1000" height="1800"></iframe>
            """, height=2000, width=1200
        )