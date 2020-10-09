import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from vega_datasets import data

st.markdown(
"""<style>
    .sidebar {flex-direction: row-reverse;}
    </style>
""", unsafe_allow_html=True)

numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
all_datasets = data.list_datasets()


def main():
    st.header("Vega Datasets explorer")
    st.sidebar.header("Configuration")

    chosen_dataset = st.sidebar.selectbox(
        "Choose a Vega dataset :", all_datasets, index=all_datasets.index("iris")
    )

    df, description, url = load_data(chosen_dataset)
    all_cols = df.columns.values
    numeric_cols = df.select_dtypes(include=numerics).columns.values
    obj_cols = df.select_dtypes(include=["object"]).columns.values

    if not description:
        st.warning("No description given")
    else:
        st.markdown(f":tada: {description}", unsafe_allow_html=True)
    st.markdown(f"URL : {url}")

    if st.sidebar.checkbox("Data preview", True):
        st.subheader("Data preview")
        st.markdown(f"Shape of dataset : {df.shape[0]} rows, {df.shape[1]} columns")
        if st.checkbox("Data types"):
            st.dataframe(df.dtypes)
        if st.checkbox("Pandas Summary"):
            st.write(df.describe())
        cols_to_style = st.multiselect(
            "Choose columns to apply BG gradient", numeric_cols
        )
        st.dataframe(df.style.background_gradient(subset=cols_to_style, cmap="BuGn"))
        st.markdown("---")

    if st.sidebar.checkbox("Plot numeric column distribution", False):
        st.subheader("Plot numeric column distribution")
        with st.echo():
            col = st.selectbox("Choose a column to display", numeric_cols)
            n_bins = st.number_input("Max number of bins ?", 5, 100, 10)
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    alt.X(f"{col}:Q", bin=alt.Bin(maxbins=n_bins)), alt.Y("count()")
                )
            )
            st.altair_chart(chart)
        st.markdown("---")

    if st.sidebar.checkbox("Scatterplot", False):
        st.subheader("Scatterplot")
        selected_cols = st.multiselect("Choose 2 columns :", numeric_cols)
        if len(selected_cols) == 2:
            color_by = st.selectbox(
                "Color by column:", all_cols, index=len(all_cols) - 1
            )
            col1, col2 = selected_cols
            chart = (
                alt.Chart(df)
                .mark_circle(size=20)
                .encode(
                    alt.X(f"{col1}:Q"), alt.Y(f"{col2}:Q"), alt.Color(f"{color_by}")
                )
                .interactive()
            )
            st.altair_chart(chart)
        st.markdown("---")

    if st.sidebar.checkbox("Classification", False):
        st.subheader("Classification")
        target = st.selectbox("Choose target :", obj_cols)

        if st.button("Run training"):
            clf, confusion_matrix = train_rf(df, numeric_cols, target)
            st.balloons()
            st.pyplot(confusion_matrix)

        st.markdown("---")

    if st.sidebar.checkbox("Regression", False):
        st.subheader("Regression")
        st.info("TODO")

    st.sidebar.header("About")
    st.sidebar.text("Made by M. Fanilo ANDRIANASOLO")
    st.sidebar.text(
        "Code : https://gist.github.com/andfanilo/6fde108467f7f07d645eb105c7a69904"
    )


def load_data(name_dataset):
    metadata = getattr(data, name_dataset.replace("-", "_"))
    df = metadata()
    description = metadata.description
    url = metadata.url
    return df, description, url


def train_rf(df, features, target):
    X = df[features]
    y = df[target].astype("category")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
    )
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    
    fig, ax = plt.subplots()
    plot_confusion_matrix(clf, X_test, y_test, ax=ax)
    return clf, fig


if __name__ == "__main__":
    main()
