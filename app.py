import os
import subprocess
import sys

# Install plotly if not already installed
try:
    import plotly
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])


# import subprocess
# import sys

import pandas as pd
import streamlit as st
import plotly.express as px



# Load Dataset
# Example: 'country' column for country names, other columns for years
data = pd.read_csv("https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/child_mortality_0_5_year_olds_dying_per_1000_born.csv")

# Melt the data to long format for easier filtering
data_melted = data.melt(id_vars=["country"], var_name="year", value_name="mortality_rate")
data_melted["year"] = pd.to_numeric(data_melted["year"])
# Streamlit App
st.title("Global Child Mortality Rate (per 1000 children born)")
st.write("By Jiya Chachan, Smeet Patel, Ji Eun Kim, Miloni Shah, Chenzhao Wang")
st.write("Dataset: Child Mortality")
st.dataframe(data) 
st.write("""Credits: https://www.gapminder.org/data/""")

st.write("""The following interactive visualization provides an insightful overview of child mortality rates (number of deaths per 1,000 live births) across countries for a selected year. 
        The data highlights disparities in healthcare, socioeconomic conditions, and development across the globe, making it a valuable tool for understanding global health challenges.""")
# Add year selection
# years = sorted(data_melted["year"].unique())  # Extract unique years from the dataset
# selected_year = st.selectbox("Select Year", years)
# Add year selection with a slider
min_year = int(data_melted["year"].min())
max_year = int(data_melted["year"].max())

st.subheader("Child Mortality Trends around the Globe")
st.write("""
This Chart reveals an important trend of how the child mortality rate have been changing across the years. 
This gives us a very important insight on how the present developed countries have successfully reduced the rate, and underdeveloped countries still faces challenges to curb child mortality successfully.
We can utilise the trends in the graph to understand the factors which might be the responsible for high mortality or low mortality. 
This will help the policymakers in developing/under-developed countries to develop data-driven policy to reduce child mortality.
""")

selected_year = st.slider("Select Year", min_value=min_year, max_value=max_year, value = 2024, step = 5)


# Filter data for the selected year
filtered_data = data_melted[data_melted["year"] == selected_year]


# Create the map
fig = px.choropleth(
    filtered_data,
    locations="country",  # Country names or ISO 3166-1 Alpha-3 codes
    locationmode="country names",  # Use 'ISO-3' if you have country codes
    color="mortality_rate",
    title=f"Child Mortality Rate in {selected_year}",
    color_continuous_scale=px.colors.sequential.OrRd,  # Customize the color scale
    
)

# Display the map
st.plotly_chart(fig)

st.write("""I began by acquiring a dataset on child mortality rates, with countries as rows and years as columns. The dataset contained child mortality rates as the number of deaths per 1,000 live births.
To make the dataset suitable for visualization, I transformed it into a long format using pandas.melt(), creating three columns: country, year, and mortality_rate. This step allowed for efficient filtering and visualization.
I chose a choropleth map because it effectively communicates regional differences using a color gradient. Each country is color-coded based on its mortality rate for a selected year, offering immediate visual insights.
I implemented a slider widget for year selection, enabling users to dynamically explore mortality rates over time.
This required ensuring that the year column was properly formatted as numeric data, and filtering the dataset based on the slider’s value.""")



