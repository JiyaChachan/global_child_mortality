import pandas as pd
import altair as alt
import streamlit as st 

# Load the data 
child_mortality = pd.read_csv("https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/child_mortality_0_5_year_olds_dying_per_1000_born.csv")  # Format: Country, Year, Value
gdp_per_capita = pd.read_csv("https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/gdp_pcap.csv")    # Format: Country, Year, Value

# Melt datasets to tidy format
child_mortality = child_mortality.melt(id_vars=["country"], var_name="year", value_name="child_mortality")
gdp_per_capita = gdp_per_capita.melt(id_vars=["country"], var_name="year", value_name="gdp_per_capita")

# Merge the datasets
merged_data = pd.merge(child_mortality, gdp_per_capita, on=["country", "year"])
merged_data["year"] = merged_data["year"].astype(int)  # Ensure 'year' is an integer

# Drop rows with missing or undefined country values
merged_data = merged_data.dropna(subset=["country"])
merged_data = merged_data[merged_data["country"] != "undefined"]

# Convert gdp_per_capita and child_mortality to numeric
merged_data["gdp_per_capita"] = pd.to_numeric(merged_data["gdp_per_capita"], errors="coerce")
merged_data["child_mortality"] = pd.to_numeric(merged_data["child_mortality"], errors="coerce")

# Drop rows with missing or invalid data
merged_data = merged_data.dropna(subset=["gdp_per_capita", "child_mortality"])

# Streamlit app
st.title("Interactive Visualization: GDP vs. Child Mortality")

st.text(" ")

st.text("The dataset represents global development indicators related to child mortality and GDP per capita for multiple countries over several years. Each row corresponds to a unique country-year combination, with the key fields being country (categorical, representing the country name), year (integer, indicating the year of data collection), child_mortality (numeric, showing the number of children under five dying per 1,000 live births), and gdp_per_capita (numeric, representing GDP per capita in constant 2017 international dollars). The dataset spans a wide range of years and countries, making it suitable for temporal and regional analyses. Missing values are present in some fields, particularly for earlier years or less-developed countries, and were handled during the data cleaning process. The values in child_mortality range from 2.24 to 756.0, while gdp_per_capita spans from $354.00 to $10,000.00, reflecting significant disparities in economic and health outcomes across countries and regions.")

st.text(" ")

# Filter data for a specific year
year = st.slider("Select Year", min_value=int(merged_data["year"].min()), max_value=int(merged_data["year"].max()), value=2024)
filtered_data = merged_data[merged_data["year"] == year]

# Select number of countries to display
num_countries = st.slider("Select Number of Countries to Display", min_value=5, max_value=50, value=30, step=5)

# Get top N countries by GDP per capita
top_countries = filtered_data.nlargest(num_countries, "gdp_per_capita")

# Create scatter plot with regression line
scatter_plot = alt.Chart(top_countries).mark_circle(size=60).encode(
    x=alt.X("gdp_per_capita:Q", scale=alt.Scale(type="log"), title="GDP per Capita (Log Scale)"),
    y=alt.Y("child_mortality:Q", title="Child Mortality (per 1,000 live births)"),
    color=alt.Color("country:N"),
    tooltip=["country", "gdp_per_capita", "child_mortality"]
).properties(
    title=f"Relationship Between GDP Per Capita and Child Mortality ({year})",
    width=800,
    height=500
)

# Add regression line
regression_line = scatter_plot.transform_regression(
    "gdp_per_capita", "child_mortality", method="linear"
).mark_line(color="red")

# Combine scatter plot and regression line
final_chart = scatter_plot + regression_line

# Display chart in Streamlit
st.altair_chart(final_chart, use_container_width=True)


st.text("To build the observatory, I began by preparing the dataset, which involved merging child mortality and GDP per capita data based on common fields: country and year. I ensured that the data was cleaned and formatted correctly, converting numerical fields like child_mortality and gdp_per_capita to numeric types and handling missing values by dropping rows with invalid entries. Once the data was ready, I created initial static visualizations using Altair to explore the relationship between GDP per capita and child mortality. The chart shows the relationship between GDP per capita and child mortality rates, highlighting an inverse trend where higher GDP per capita generally corresponds to lower child mortality. Building on this foundation, I added interactivity through Streamlit, allowing users to dynamically filter the dataset by year and select the number of countries to display. To enhance the visual analysis, I overlaid a regression line on the scatter plot, which provides a clear representation of trends. The app's functionality was refined iteratively, incorporating sliders for user interaction and tooltips for exploring country-specific data points.")
