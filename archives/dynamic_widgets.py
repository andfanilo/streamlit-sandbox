import altair as alt
import streamlit as st
from vega_datasets import data

cars = data.cars()

quantitative_variables = [
    "Miles_per_Gallon",
    "Cylinders",
    "Displacement",
    "Horsepower",
    "Weight_in_lbs",
    "Acceleration",
]


@st.cache
def get_y_vars(dataset, x, variables):
    corrs = dataset.corr()[x]
    remaining_variables = [v for v in variables if v != x]
    sorted_remaining_variables = sorted(
        remaining_variables, key=lambda v: corrs[v], reverse=True
    )
    format_dict = {v: f"{v} ({corrs[v]:.2f})" for v in sorted_remaining_variables}
    return sorted_remaining_variables, format_dict


st.header("Cars Dataset - Correlation Dynamic Dropdown")
x = st.selectbox("x", quantitative_variables)
y_options, y_formats = get_y_vars(cars, x, quantitative_variables)
y = st.selectbox(
    f"y (sorted by correlation with {x})", y_options, format_func=y_formats.get
)

plot = alt.Chart(cars).mark_circle().encode(x=x, y=y)

st.altair_chart(plot)
