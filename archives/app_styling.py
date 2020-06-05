import pandas as pd
import streamlit as st 

# https://stackoverflow.com/questions/43596579/how-to-use-python-pandas-stylers-for-coloring-an-entire-row-based-on-a-given-col

df = pd.read_csv("data/titanic.csv")

def highlight_survived(s):
    return ['background-color: green']*len(s) if s.Survived else ['background-color: red']*len(s)

def color_survived(val):
    color = 'green' if val else 'red'
    return f'background-color: {color}'

st.dataframe(df.style.apply(highlight_survived, axis=1))
st.dataframe(df.style.applymap(color_survived, subset=['Survived']))