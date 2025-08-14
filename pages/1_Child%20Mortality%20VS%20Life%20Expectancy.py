import pandas as pd
import streamlit as st
import altair as alt

child_mortality = pd.read_csv("https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/child_mortality_0_5_year_olds_dying_per_1000_born.csv")
life_expectancy = pd.read_csv("https://huggingface.co/spaces/jiyachachan/fp2/resolve/main/life_expectancy.csv")

st.title("Interactive Observatory: Child Mortality & Life Expectancy")
st.write("""
For this analysis, I selected Argentina, Australia, China, India, South Africa, the UK,
and the USA as representative countries for different global regions. These countries 
highlight diverse economic, social, and historical contexts, making them ideal for 
observing trends in child mortality and life expectancy. The time period of 1900 to
2024 was chosen as it encompasses rapid global industrialization, the rise of modern 
medicine, and recent advancements in healthcare and living standards, while also including 
years with limited historical data to provide a broader context.
""")

countries = list(child_mortality['country'].unique())
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=["Argentina", "Australia", "China", "India", "South Africa", "UK", "USA"])
year_range = st.sidebar.slider("Select Year Range", 1900, 2024, (1900, 2024))

filtered_mortality = child_mortality[child_mortality['country'].isin(selected_countries)]
filtered_expectancy = life_expectancy[life_expectancy['country'].isin(selected_countries)]
years = [str(year) for year in range(year_range[0], year_range[1] + 1)]
filtered_mortality = filtered_mortality[['country'] + years]
filtered_expectancy = filtered_expectancy[['country'] + years]

def melt_dataframe(df, value_name):
    df_melted = df.melt(id_vars=["country"], var_name="year", value_name=value_name)
    df_melted["year"] = df_melted["year"].astype(int)
    return df_melted

mortality_melted = melt_dataframe(filtered_mortality, "Child Mortality")
expectancy_melted = melt_dataframe(filtered_expectancy, "Life Expectancy")

# Chart 1: Child Mortality Trends
st.subheader("Chart 1: Child Mortality Trends")
st.write("""
This chart reveals significant regional disparities in child mortality rates across the 
selected countries. For instance, India and South Africa initially exhibit much higher 
mortality rates compared to developed nations like the USA and the UK, reflecting disparities 
in healthcare access. Notably, the chart captures periods of global crises such as pandemics 
or wars, where temporary spikes in child mortality rates can be observed, such as in South 
Africa during the mid-20th century. Over time, all countries demonstrate a marked decline, 
indicating progress in global health and development.
""")

mortality_chart = alt.Chart(mortality_melted).mark_line().encode(
    x=alt.X("year:O", title="Year"),
    y=alt.Y("Child Mortality:Q", title="Child Mortality (0–5 years per 1000 births)"),
    color="country:N"
).properties(width=700, height=400)

st.altair_chart(mortality_chart)

# Chart 2: Life Expectancy Trends
st.subheader("Chart 2: Life Expectancy Trends")
st.write("""
This visualization shows how life expectancy has improved across all regions, with 
countries like the UK and the USA maintaining consistently higher life expectancy, 
while developing nations such as India and South Africa only recently catching up. 
However, fluctuations are visible, notably during the 1918 influenza pandemic and 
the global conflicts of the 20th century, where life expectancy briefly plummeted. 
Interestingly, the sharp rise in life expectancy in countries like China during the
mid-20th century reflects public health reforms and economic growth.
""")

expectancy_chart = alt.Chart(expectancy_melted).mark_line().encode(
    x=alt.X("year:O", title="Year"),
    y=alt.Y("Life Expectancy:Q", title="Life Expectancy at Birth"),
    color="country:N"
).properties(width=700, height=400)

st.altair_chart(expectancy_chart)

# Chart 3: Child Mortality vs. Life Expectancy
st.subheader("Chart 3: Child Mortality vs. Life Expectancy")
st.write("""
This scatter plot illustrates the strong inverse relationship between child mortality 
rates and life expectancy at birth, underscoring how advancements in healthcare, 
nutrition, and living conditions improve both indicators simultaneously. A particularly 
striking observation is how the data for countries like India and South Africa forms a 
steep curve, signifying rapid improvements in life expectancy as child mortality declines. 
Developed nations such as Australia and the USA show a plateau in the later stages, where 
child mortality rates are already low, and life expectancy improvements are incremental. 
The trajectory of China’s data during the mid-20th century highlights a rapid transition, 
likely due to systemic public health efforts.
""")

merged_data = pd.merge(mortality_melted, expectancy_melted, on=["country", "year"])
scatter_chart = alt.Chart(merged_data).mark_circle(size=60).encode(
    x=alt.X("Life Expectancy:Q", title="Life Expectancy at Birth"),
    y=alt.Y("Child Mortality:Q", title="Child Mortality (0–5 years per 1000 births)"),
    color="country:N",
    tooltip=["country", "year", "Child Mortality", "Life Expectancy"]
).properties(width=700, height=400)

st.altair_chart(scatter_chart)