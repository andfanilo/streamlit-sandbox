import numpy as np
import pandas as pd

import altair as alt
#import altair.vega.v5 as alt
from vega_datasets import data

import streamlit as alt

source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
})

chart = alt.Chart(
    data=alt.UrlData(
        url='https://vega.github.io/vega-datasets/data/cars.json'
    ),
    mark='point',
    encoding=alt.FacetedEncoding(
        x=alt.PositionFieldDef(
            field='Horsepower',
            type='quantitative'
        ),
        y=alt.PositionFieldDef(
            field='Miles_per_Gallon',
            type='quantitative'
        ),
        color=alt.StringFieldDefWithCondition(
            field='Origin',
            type='nominal'
        )
    ),
    config=alt.Config(
        view=alt.ViewConfig(
            continuousHeight=300,
            continuousWidth=400
        )
    )
)

st.altair_chart(chart)