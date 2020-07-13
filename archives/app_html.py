import streamlit.components.v1 as components

with open('app.html') as f:
    data = f.read()
    components.html(data)