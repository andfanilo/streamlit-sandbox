"""Adds an st.rerun() command to Streamlit.
https://gist.github.com/tvst/58c42300d3b6de48e805af7429cac2e7

Usage:
  import streamlit as st
  import st_rerun_patch
  
  # ...
  
  st.rerun()

"""
import streamlit as st
from streamlit.ScriptRequestQueue import RerunData
from streamlit.ScriptRunner import RerunException
from streamlit.server.Server import Server
import streamlit.ReportThread as ReportThread


def rerun():
    """Rerun a Streamlit app from the top!"""
    widget_states = _get_widget_states()
    raise RerunException(RerunData(widget_states))


def _get_widget_states():
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_infos.values()

    for session_info in session_infos:
        if session_info.session._main_dg == ctx.main_dg:
            session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')
    # Got the session object!

    return session._widget_states

    ctx = ReportThread.get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_infos.values()

    for session_info in session_infos:
        if session_info.session._main_dg == ctx.main_dg:
            session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')
    # Got the session object!

    return session._widget_states


st.rerun = rerun