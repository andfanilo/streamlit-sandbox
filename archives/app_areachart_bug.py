import datetime as dt

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

chart_data = pd.DataFrame([[1, 2, 1], [0, 2, 1], [1, 3, 5]],
                          columns=['a', 'b', 'c'],
                          index=[1, 2, 3])
st.area_chart(chart_data)

melted_chart_data = pd.melt(chart_data.reset_index(), id_vars=["index"])
st.altair_chart(
       alt.Chart(melted_chart_data, width=640).mark_area().encode(
              alt.X("index", title=""),
              alt.Y("value", title="", stack=True),
              alt.Color("variable", title="", type="nominal"),
              opacity={"value": 0.7},
              tooltip=["index", "value", "variable"]
       ).interactive()
)
st.dataframe(melted_chart_data)



chart_data_dt = pd.DataFrame([[1, 2, 1], [0, 2, 1], [1, 3, 5]],
                          columns=['a', 'b', 'c'],
                          index=[dt.datetime(2017, 1, 1),
                                 dt.datetime(2018, 1, 2),
                                 dt.datetime(2019, 1, 3)])
st.area_chart(chart_data_dt)
melted_chart_data_dt = pd.melt(chart_data_dt.reset_index(), id_vars=["index"])
st.altair_chart(
       alt.Chart(melted_chart_data_dt, width=720).mark_area().encode(
              alt.X("index", title="", scale=alt.Scale(type="utc")),
              alt.Y("value", title="", scale=alt.Scale(type="utc"), stack=None),
              alt.Color("variable", title="", type="nominal"),
              opacity={"value": 0.7},
              tooltip=["index", "value", "variable"]
       )
)
st.dataframe(melted_chart_data_dt)
