import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('data/Filtered_Accident_Causes__Alcohol_Focus_.csv')

# Show available columns (for debugging)

# Ensure session state for shared filtering across pages
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df.copy()
    st.session_state.years = (int(df["Year"].min()), int(df["Year"].max()))
    st.session_state.genres = []

# Sidebar filtering controls
if "Year" in df.columns:
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())

    st.sidebar.header("Filter Options")
    selected_years = st.sidebar.slider("Years", min_year, max_year, st.session_state.years)
    selected_genres = st.sidebar.multiselect(
        "Filter by Main Cause", df["Main Cause"].unique(), default=st.session_state.genres
    )

    apply_filter = st.sidebar.button("Apply Filter")
    reset_filter = st.sidebar.button("Reset")

    if apply_filter:
        df_year_filtered = df[df["Year"].between(selected_years[0], selected_years[1])]
        if selected_genres:
            st.session_state.filtered_df = df_year_filtered[
                df_year_filtered["Main Cause"].isin(selected_genres)
            ]
        else:
            st.session_state.filtered_df = df_year_filtered
        st.session_state.years = selected_years
        st.session_state.genres = selected_genres

    elif reset_filter:
        st.session_state.filtered_df = df.copy()
        st.session_state.years = (min_year, max_year)
        st.session_state.genres = []

# === Trend Visualization ===
st.title("📈 Yearly Trend of Accident Causes")

# Dropdown for cause selection
available_causes = st.session_state.filtered_df["Main Cause"].dropna().unique()
selected_cause = st.selectbox("Select a Cause to View Trend", sorted(available_causes))

# Clean input for robust filtering
selected_cause_clean = selected_cause.strip().lower()
cause_df = st.session_state.filtered_df[
    st.session_state.filtered_df["Main Cause"].str.strip().str.lower() == selected_cause_clean
]

# Check for empty result
if cause_df.empty:
    st.warning(f"No data found for cause: '{selected_cause}' in selected filters.")
else:
    # Group by Year safely
    if "Year" in cause_df.columns:
        cause_per_year = (
            cause_df.groupby("Year")
            .size()
            .reset_index(name="Incident Count")
            .sort_values("Year")
        )

        # Show final columns (debugging)
       
       

        # Plot line chart
        fig_line = px.line(
            cause_per_year,
            x="Year",
            y="Incident Count",
            title=f"Yearly Trend: {selected_cause}",
            markers=True,
            labels={"Year": "Year", "Incident Count": "Incidents"}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.error("❌ 'Year' column is missing from the dataset.")
