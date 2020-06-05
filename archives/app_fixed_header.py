import streamlit as st

html_code = """
<style>
body { margin: 0; font-family: Arial, Helvetica, sans-serif;} 
.header{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;top:0;} 
.sticky { position: fixed; top: 0; width: 100%;} 
</style>

<div class="header" id="myHeader">42</div> 
"""

st.write(html_code, unsafe_allow_html=True)
for _ in range(100):
    st.write("Hello")
