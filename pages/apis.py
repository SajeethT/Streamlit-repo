import streamlit as st
import requests

st.title("API Page")

url = st.text_input("Paste URL")

if st.button("Fetch Data"):
    try:
        response = requests.get(url).json()
        
        st.json(response, expanded=True)   

    except Exception as e:
        st.write(f"❌ Error: {e}")