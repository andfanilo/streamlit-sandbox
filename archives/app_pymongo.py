import random
import time

from pymongo import MongoClient
import streamlit as st


def main():
    st.title('Pymongo test')
    client = get_mongo_connection()
    st.sidebar.header("Configuration")
    artist = st.sidebar.selectbox("Select artist", ('Fanilo', 'Rolling Stones'))

    arr = []
    chart = st.empty()
    
    while True:
        time.sleep(1)
        r = get_recording(client, artist)
        arr.append(r['price'])
        chart.line_chart(arr[:10])


@st.cache(allow_output_mutation=True)
def get_mongo_connection():
    client = MongoClient()
    return client


def get_recording(client: MongoClient, artist: str):
    db = client.test
    return db.recordings.find_one({"artist": artist})


if __name__ == "__main__":
    main()