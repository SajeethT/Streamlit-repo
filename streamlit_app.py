
import streamlit as st

pages ={
    "My Stuff":
 [ 
    st.Page("pages/accident.py", title="Accidents"),
    st.Page("pages/Graph.py", title="Graphs"),
    
    
    
 ]
}
pg = st.navigation(pages)
pg.run()