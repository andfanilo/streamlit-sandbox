import json
import geopandas as gpd
import altair as alt
import streamlit as st

test = gpd.read_file('data/oakland/Oak_CityCouncilDistricts.shp')
inline_data = alt.InlineData(format=alt.JsonDataFormat(property = 'features'), values=json.loads(test.to_json()))
chart = alt.Chart(inline_data).mark_geoshape()
st.vega_lite_chart(chart.to_dict())
