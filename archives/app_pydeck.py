import altair as alt
from vega_datasets import data
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/bart-lines.json"
df = pd.read_json(DATA_URL)

#st.dataframe(df)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

df['color'] = df['color'].apply(hex_to_rgb)

view_state = pdk.ViewState(
    latitude=37.782556,
    longitude=-122.3484867,
    zoom=10
)

layer = pdk.Layer(
    type='PathLayer',
    data=df,
    pickable=True,
    get_color='color',
    width_scale=20,
    width_min_pixels=2,
    get_path='path',
    get_width=5
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={'text': '{name}'})

#st.pydeck_chart(r)

import altair as alt
from vega_datasets import data

states = alt.topo_feature(data.us_10m.url, feature='states')

line_source = pd.DataFrame({
    'longitude': [-122.3093131, -122.3748433, -118.4080744],
    'latitude': [47.44898194, 37.61900194, 33.94253611],
    'order': [1,2,3]
})

background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=800,
    height=500
).project('albersUsa')
point_path = line_path = alt.Chart(line_source).mark_circle().encode(
    longitude="longitude:Q",
    latitude="latitude:Q",
    size=alt.value(60)
)
line_path = alt.Chart(line_source).mark_line().encode(
    longitude="longitude:Q",
    latitude="latitude:Q",
    order='order:O'
)

st.altair_chart((background + point_path + line_path))