import streamlit as st
import requests
import pandas as pd

st.title("Campus Admission data")

#url = st.text_input("Paste URL with campus and API key")
base_url = 'https://special-invention-v66rgrj4xvr5hxg7r-5000.app.github.dev'
campus_search_endpoint = '/api/v1/campus/'

api_key = st.text_input("Your API key")

campus = st.selectbox(
    "Choose campus",
    ("Berkeley", "Davis", "Los Angeles", "Merced", "Riverside",  "San Diego", "Santa Barbara", "Santa Cruz"),
)

if st.button("Fetch Campus Data"):
    try:

        chosen_campus = campus.lower()
        fetch_url = base_url+campus_search_endpoint+chosen_campus+"?key="+api_key
        data = requests.get(fetch_url).json()
        
        st.json(data, expanded=True)   

        tab1, tab2, tab3 = st.tabs(["Overview", "Demographics", "Feeder Schools"])
 

        admissions = data["admissions"]
        demographics = data["demographic_totals"]
        top_feeder_schools = data["top_feeder_schools"]

        with tab1:
            # Admissions overview
            st.header(f"UC {data['university'].capitalize()} Admissions Data")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Applied", admissions["total_applied"])
            col2.metric("Total Accepted", admissions["total_accepted"])
            col3.metric("Total Enrolled", admissions["total_enrolled"])

        with tab2:

            st.header(f"UC {data['university'].capitalize()} Demographics")
            # Demographics
            demo_df = pd.DataFrame(demographics).T
            st.subheader("Demographics Breakdown")
            st.dataframe(demo_df)
            st.divider()
            st.bar_chart(demo_df[["applied", "admitted", "enrolled"]])

        with tab3:

            # Feeder schools
            st.header(f"UC {data['university'].capitalize()} Feeder Schools")
            schools_df = pd.DataFrame(top_feeder_schools)
            st.subheader("Top Feeder Schools")
            st.dataframe(schools_df)
            st.divider()
            st.bar_chart(schools_df.set_index("school")["total_enrolled"])

       

    except Exception as e:
        st.write(f"❌ Error: {e}")


