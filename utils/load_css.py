"""
https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/25
"""

import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def remote_css(url):
    st.markdown('<style src="{}"></style>'.format(url), unsafe_allow_html=True)

def icon_css(icone_name):
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

def icon(icon_name):
    st.markdown('<i class="material-icons">{}</i>'.format(icon_name), unsafe_allow_html=True)
