import streamlit as st
import pandas as pd
import altair as alt

income_df = pd.read_csv('https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/mincpcap_cppp.csv')
mortality_df = pd.read_csv('https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/child_mortality_0_5_year_olds_dying_per_1000_born.csv')

income_long = pd.melt(income_df, id_vars=['country'], var_name='year', value_name='income')
mortality_long = pd.melt(mortality_df, id_vars=['country'], var_name='year', value_name='mortality')

income_long['year'] = income_long['year'].astype(int)
mortality_long['year'] = mortality_long['year'].astype(int)

yay = pd.merge(income_long, mortality_long, on=['country', 'year'])

yer = yay.dropna()
yer = yer[yer["year"] <= 2024]

st.title("Child Mortality vs Daily Income")

st.text("From our earlier exploration of the data from part 1, we cleaned the data, where we removed around 2500 missing values which we deemed to not make a significant difference. Furthermore, we made sure to change the data appropriately such as changing the data type for the year into an integer. We also filtered the data so the max year is 2024, as the dataset included projected quantities for future years.")
st.text("We examine child mortality deaths as our y-variable and daily income as our x-variable. The average daily income is the mean daily household per capita income. The mortality rate is the death of children under five years of age per 1000 live births. After cleaning the dataset, it contains 57195 rows × 4 columns with country, year, income, and mortality.")
yeyear = st.slider("Select a Year", min_value=yer["year"].min(), max_value=2024, value=2024)

filtered_yer = yer[yer["year"] == yeyear]

scatter_plot = alt.Chart(filtered_yer).mark_circle(size=60).encode(
    x=alt.X('income', title='Daily Income (USD)', scale=alt.Scale(type='log')),
    y=alt.Y('mortality', title='Child Mortality (per 1,000)'),
    color='country',
    tooltip=['country', 'year', 'income', 'mortality']
).properties(
    width=700,
    height=500,
    title=f"Child Mortality vs Daily Income in {yeyear}"
)

st.altair_chart(scatter_plot, use_container_width=True)

st.text("In Streamlit, we create an interactive slider that allows the user to choose a year where the earliest year is 1800 and the maximum year is 2024. In Altair, we create a scatter plot where the x-axis is represented by daily income (USD) set to a logarithmic scale for better visualization for larger income ranges, and the y-axis is represented by child mortality (per 1,000). Each country is assigned a unique color and we incorporate a hover tooltip to show the country, year, income, and mortality rate for a specific data point.")