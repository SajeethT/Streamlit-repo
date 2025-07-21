import requests
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚗 Traffic Incidents Dashboard")

# Load data
df = pd.read_csv('data/Filtered_Accident_Causes__Alcohol_Focus_.csv')

# Initialize session state for filtering
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df.copy()
    st.session_state.years = (int(df["Year"].min()), int(df["Year"].max()))
    st.session_state.genres = []
    

# Sidebar Filters
if "Year" in df.columns:
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())

    st.sidebar.header("Filter Options")
    selected_years = st.sidebar.slider("Years", min_year, max_year, st.session_state.years)
    selected_genres = st.sidebar.multiselect("Filter by Main Cause", df["Main Cause"].unique(), default=st.session_state.genres)

    apply_filter = st.sidebar.button("Apply Filter")
    reset_filter = st.sidebar.button("Reset")

    if apply_filter:
        df_year_filtered = df[df["Year"].between(selected_years[0], selected_years[1])]
        if selected_genres:
            st.session_state.filtered_df = df_year_filtered[df_year_filtered["Main Cause"].isin(selected_genres)]
        else:
            st.session_state.filtered_df = df_year_filtered
        st.session_state.years = selected_years
        st.session_state.genres = selected_genres

    elif reset_filter:
        st.session_state.filtered_df = df.copy()
        st.session_state.years = (min_year, max_year)
        st.session_state.genres = []

    # Display filtered data
    st.write("### Filtered Data")
    st.dataframe(st.session_state.filtered_df, use_container_width=True)

    # Pie chart
    st.subheader("Accident Causes Distribution")
    cause_counts = (
        st.session_state.filtered_df["Main Cause"]
        .value_counts()
        .reset_index()
    )
    cause_counts.columns = ["Main Cause", "Incident Count"]
    fig = px.pie(
        cause_counts,
        names="Main Cause",
        values="Incident Count",
        title="Distribution of Accident Causes",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("The dataset must contain a 'Year' column.")


