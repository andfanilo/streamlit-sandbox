import streamlit as st
import utils.st_state_patch
import utils.st_rerun_patch

st.title("Testing State")

s = st.State(key="user metadata")

if not s:
    # Initialize it here!
    s.page = 0

if s.page == 0:
    s.input = st.text_input("Input text for next page")
    if s.input:
        s.page = 1
        #st.rerun()

if s.page == 1:
    st.markdown(f"Retrieve input from state {s.input}")
    