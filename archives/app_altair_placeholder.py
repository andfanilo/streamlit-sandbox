import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.header("Demo placeholder altair chart")

df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c']
)

chart_placeholder = st.empty()

color = st.radio("select color", ("blue", 'red', 'green'))

c = alt.Chart(df).mark_circle().encode(
    x='a',
    y='b',
    color=alt.value(color),
    size='c'
)

chart_placeholder.altair_chart(c)
