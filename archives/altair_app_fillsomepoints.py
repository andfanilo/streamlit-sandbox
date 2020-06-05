import random
import altair as alt
import pandas as pd
import streamlit as st 

df = pd.DataFrame({
  'date': pd.date_range(start='2020-01-01', end='2020-01-31'),
  'OLS': [random.randint(0, 1) for x in range(31)],
  'OLS2': [random.randint(0, 10) for x in range(31)],
  'OLS3_nopoint': [random.randint(0, 100) for x in range(31)]
}).melt(id_vars='date', var_name="OLS", value_name="value")

df['opacity'] = 0
df.loc[df['OLS']!="OLS3_nopoint", 'opacity'] = 1

base = alt.Chart(df).encode(
  x="date:T",
  y="value:Q",
  color='OLS:N'
)
lines = base.mark_line()
points = base.mark_point(filled=True).encode(
  opacity=alt.Opacity("opacity:N", legend=None)
)
st.altair_chart(lines + points, use_container_width=True)