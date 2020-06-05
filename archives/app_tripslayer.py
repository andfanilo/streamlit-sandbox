import altair as alt
from vega_datasets import data
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit_nightly as st

TRIPS_LAYER_DATA  = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/sf.trips.json"

df = pd.read_json(TRIPS_LAYER_DATA)

df["coordinates"] = df["waypoints"].apply(lambda f: [item["coordinates"] for item in f])
df["timestamps"] = df["waypoints"].apply(lambda f: [item["timestamp"] - 1554772579000 for item in f])

df.drop(["waypoints"], axis=1, inplace=True)

st.write(df)

layer = pdk.Layer(
    "TripsLayer",
    df,
    get_path="coordinates",
    get_timestamps="timestamps",
    get_color=[253, 128, 93],
    opacity=1,
    width_min_pixels=10,
    rounded=True,
    trail_length=600,
    current_time=500,
)

view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=11, bearing=0, pitch=45)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(r)