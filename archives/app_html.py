from jinja2 import Environment, FileSystemLoader
import streamlit.components.v1 as components
import streamlit as st 

st.title("Hello Lottie-web !")
loop = st.checkbox("Loop animation", True)

with open('data.json') as json_file:
    lottie_data = json_file.read()

env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template.html.jinja')
html_data = template.render(data=lottie_data, loop=str(loop).lower())

components.html(html_data, height=800)