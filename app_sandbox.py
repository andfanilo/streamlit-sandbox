import numpy as np
import streamlit as st
import plotly.express as px

SIDE = 2000
fig = px.imshow(np.random.randint(0, 256, (SIDE, SIDE, 3), dtype=np.uint8))
st.plotly_chart(fig, use_container_width=True)