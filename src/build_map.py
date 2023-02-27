import folium
import pandas as pd

# Cleaning the data.
df = pd.read_csv("../data/horror_films.csv")
df.drop_duplicates(inplace=True)
table = pd.pivot_table(data=df,index='Setting', values='Film', aggfunc='count')
table.to_csv("../data/cleaned_horror_films.csv")

# Creating the map.
m = folium.Map(location=[40, -95],zoom_start=4, tiles='Stamen Toner')
STATE_GEO = "../data/us_states.json"
DATA_CSV = "../data/cleaned_horror_films.csv"
DATA_CSV_PD = pd.read_csv(DATA_CSV)

folium.Choropleth(
    geo_data=STATE_GEO,
    name="TK",
    data=DATA_CSV_PD,
    columns=["Setting", "Film"],
    key_on="feature.id",
    fill_color="Reds",
    fill_opacity=0.7,
    line_opacity=.1,
    nan_fill_color="white",
    highlight='True',
    legend_name="Number of horror films per state",
).add_to(m)

folium.LayerControl().add_to(m)
m.save("../us_horror_films.html")
