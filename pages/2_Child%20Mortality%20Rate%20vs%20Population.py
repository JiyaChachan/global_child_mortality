import streamlit as st
import pandas as pd
import altair as alt

# Load data
child_mortality_path = "child_mortality_0_5_year_olds_dying_per_1000_born.csv"
population_path = "pop.csv"

child_mortality = pd.read_csv(child_mortality_path)
population = pd.read_csv(population_path)

# Data Cleaning
def convert_population(value):
    if isinstance(value, str):
        if 'B' in value:
            return float(value.replace('B', '')) * 1_000_000_000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1_000_000
        elif 'k' in value:
            return float(value.replace('k', '')) * 1_000
        else:
            return float(value)
    return value

population.iloc[:, 1:] = population.iloc[:, 1:].applymap(convert_population)

# Title and Description
st.title("Child Mortality Rate vs Population")

st.write("""
    This visualization explores the relationship between child mortality rates (per 1,000 live births) and population size for a selected country over time. 
    By displaying both metrics side-by-side on a dual-y-axis chart, the visual aims to provide insights into how population trends and child mortality rates have evolved across decades.
    The visualization is interactive, allowing users to select a country from the dropdown menu. This enables tailored exploration of trends specific to different countries.
    Hovering over the chart provides tooltips with detailed information for each data point, including the year, population size, and child mortality rate.
""")

st.subheader("Select a Country")
countries = sorted(child_mortality['country'].unique())
selected_country = st.selectbox("Country", countries, index=0)

if selected_country:
   
    mortality_country = child_mortality[child_mortality['country'] == selected_country].melt(
        id_vars='country', var_name='year', value_name='child_mortality'
    )
    population_country = population[population['country'] == selected_country].melt(
        id_vars='country', var_name='year', value_name='population'
    )

    merged_country_data = pd.merge(mortality_country, population_country, on=['country', 'year'], how='inner')
    merged_country_data['year'] = merged_country_data['year'].astype(int)
    merged_country_data = merged_country_data[merged_country_data['year'] % 20 == 0]

    # Dual-Y Axis Chart
    dual_axis_chart = alt.layer(
        # First Layer: Child Mortality
        alt.Chart(merged_country_data).mark_line(point=True).encode(
            x=alt.X('year:O', title='Year (Every 20 Years)', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('child_mortality:Q', title='Child Mortality Rate (per 1,000 live births)', axis=alt.Axis(titleColor='lightblue')),
            tooltip=['year', 'child_mortality']
        ).properties(
            width=800,
            height=400,
        ),
        # Second Layer: Population
        alt.Chart(merged_country_data).mark_line(color='orange', point=True).encode(
            x=alt.X('year:O'),
            y=alt.Y('population:Q', title='Population (in millions)', axis=alt.Axis(titleColor='orange')),
            tooltip=['year', 'population']
        )
    ).resolve_scale(
        y='independent'
    ).properties(
        title=f" Child Mortality and Population Trends in {selected_country}"
    )

    st.altair_chart(dual_axis_chart, use_container_width=True)

st.write("""
Initially, I planned to calculate the child mortality rate per population as a combined metric to represent both trends in one graph. However, this approach proved misleading because large populations could distort the results, masking the distinct trends of each metric. As a solution, I switched to a dual-axis chart, separating child mortality (per 1,000 live births) and population size (in millions) into independent axes. This made the comparison clearer, improved interpretability, and allowed for better interactivity and analysis of the two trends over time.
""")