"""Bokeh Visualization Template

This template is a general outline for turning your data into a 
visualization using Bokeh.
"""
import numpy as np
import pandas as pd
import streamlit as st
from bokeh.io import output_file
from bokeh.layouts import column
from bokeh.layouts import gridplot
from bokeh.layouts import row
from bokeh.models import CategoricalColorMapper
from bokeh.models import CDSView
from bokeh.models import ColumnDataSource
from bokeh.models import Div
from bokeh.models import GroupFilter
from bokeh.models import HoverTool
from bokeh.models import NumeralTickFormatter
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.plotting import figure
from bokeh.plotting import reset_output
from vega_datasets import data

# Reset plots between Streamlit runs
reset_output()

st.header("Interactive Data Visualization in Python With Bokeh")
st.sidebar.markdown(
    "From [Interactive Data Visualization in Python With Bokeh](https://realpython.com/python-data-visualization-bokeh/)"
)

# Prepare the data
@st.cache()
def load_data():
    player_stats = pd.read_csv(
        "data/nba/2017-18_playerBoxScore.csv", parse_dates=["gmDate"]
    )
    team_stats = pd.read_csv(
        "data/nba/2017-18_teamBoxScore.csv", parse_dates=["gmDate"]
    )
    standings = pd.read_csv("data/nba/2017-18_standings.csv", parse_dates=["stDate"])
    return player_stats, team_stats, standings


player_stats, team_stats, standings = load_data()

# Organize sidebar

page_list = (
    "Show data",
    "Plot competition",
    "Plot 3-pointers",
    "Philadelphia Win-Loss",
)

st.sidebar.subheader("Administration")
select_page = st.sidebar.selectbox("Choose a page", page_list)

if select_page == page_list[0]:
    st.dataframe(player_stats.head(5))
    st.dataframe(team_stats.head(5))
    st.dataframe(standings.head(5))

if select_page == page_list[1]:
    st.subheader("Visualize the west teams")

    west_top_2 = (
        standings[(standings["teamAbbr"] == "HOU") | (standings["teamAbbr"] == "GS")]
        .loc[:, ["stDate", "teamAbbr", "gameWon"]]
        .sort_values(["teamAbbr", "stDate"])
    )

    west_fig = figure(
        x_axis_type="datetime",
        plot_height=300,
        plot_width=800,
        title="Western Conference Top 2 Teams Wins Race, 2017-18",
        x_axis_label="Date",
        y_axis_label="Wins",
        toolbar_location=None,
    )

    east_fig = figure(
        x_axis_type="datetime",
        plot_height=300,
        plot_width=800,
        title="Eastern Conference Top 2 Teams Wins Race, 2017-18",
        x_axis_label="Date",
        y_axis_label="Wins",
        toolbar_location=None,
    )

    west_fig.legend.location = "top_left"
    east_fig.legend.location = "top_left"

    # Connect to and draw the data
    west_cds = ColumnDataSource(west_top_2)
    rockets_view = CDSView(
        source=west_cds, filters=[GroupFilter(column_name="teamAbbr", group="HOU")]
    )
    warriors_view = CDSView(
        source=west_cds, filters=[GroupFilter(column_name="teamAbbr", group="GS")]
    )

    standings_cds = ColumnDataSource(standings)
    celtics_view = CDSView(
        source=standings_cds, filters=[GroupFilter(column_name="teamAbbr", group="BOS")]
    )
    raptors_view = CDSView(
        source=standings_cds, filters=[GroupFilter(column_name="teamAbbr", group="TOR")]
    )

    west_fig.step(
        "stDate",
        "gameWon",
        source=west_cds,
        view=rockets_view,
        color="#CE1141",
        legend="Rockets",
    )
    west_fig.step(
        "stDate",
        "gameWon",
        source=west_cds,
        view=warriors_view,
        color="#006BB6",
        legend="Warriors",
    )

    east_fig.step(
        "stDate",
        "gameWon",
        color="#007A33",
        legend="Celtics",
        source=standings_cds,
        view=celtics_view,
    )
    east_fig.step(
        "stDate",
        "gameWon",
        color="#CE1141",
        legend="Raptors",
        source=standings_cds,
        view=raptors_view,
    )

    # Organize the layout
    east_panel = Panel(child=east_fig, title="Eastern Conference")
    west_panel = Panel(child=west_fig, title="Western Conference")
    chart = Tabs(tabs=[west_panel, east_panel])

    # Preview and save
    st.bokeh_chart(chart)

if select_page == page_list[2]:
    # Find players who took at least 1 three-point shot during the season
    three_takers = player_stats[player_stats["play3PA"] > 0]

    # Clean up the player names, placing them in a single column
    three_takers["name"] = [
        f'{p["playFNm"]} {p["playLNm"]}' for _, p in three_takers.iterrows()
    ]

    # Aggregate the total three-point attempts and makes for each player
    three_takers = (
        three_takers.groupby("name")
        .sum()
        .loc[:, ["play3PA", "play3PM"]]
        .sort_values("play3PA", ascending=False)
    )

    # Filter out anyone who didn't take at least 100 three-point shots
    three_takers = three_takers[three_takers["play3PA"] >= 100].reset_index()

    # Add a column with a calculated three-point percentage (made/attempted)
    three_takers["pct3PM"] = three_takers["play3PM"] / three_takers["play3PA"]

    three_takers_cds = ColumnDataSource(three_takers)
    select_tools = ["box_select", "lasso_select", "poly_select", "tap", "reset"]
    three_takers_fig = figure(
        plot_height=400,
        plot_width=600,
        x_axis_label="Three-Point Shots Attempted",
        y_axis_label="Percentage Made",
        title="3PT Shots Attempted vs. Percentage Made (min. 100 3PA), 2017-18",
        toolbar_location="below",
        tools=select_tools,
    )

    # Format the y-axis tick labels as percentages
    three_takers_fig.yaxis[0].formatter = NumeralTickFormatter(format="00.0%")

    # Add square representing each player
    three_takers_fig.square(
        x="play3PA",
        y="pct3PM",
        source=three_takers_cds,
        color="royalblue",
        selection_color="deepskyblue",
        nonselection_color="lightgray",
        nonselection_alpha=0.3,
    )

    tooltips = [
        ("Player", "@name"),
        ("Three-Pointers Made", "@play3PM"),
        ("Three-Pointers Attempted", "@play3PA"),
        ("Three-Point Percentage", "@pct3PM{00.0%}"),
    ]
    hover_glyph = three_takers_fig.circle(
        x="play3PA",
        y="pct3PM",
        source=three_takers_cds,
        size=15,
        alpha=0,
        hover_fill_color="red",
        hover_alpha=0.5,
    )

    three_takers_fig.add_tools(HoverTool(tooltips=tooltips, renderers=[hover_glyph]))

    st.bokeh_chart(three_takers_fig)

if select_page == page_list[3]:
    # Isolate relevant data
    phi_gm_stats = (
        team_stats[
            (team_stats["teamAbbr"] == "PHI") & (team_stats["seasTyp"] == "Regular")
        ]
        .loc[:, ["gmDate", "teamPTS", "teamTRB", "teamAST", "teamTO", "opptPTS",]]
        .sort_values("gmDate")
    )

    # Add game number
    phi_gm_stats["game_num"] = range(1, len(phi_gm_stats) + 1)

    # Derive a win_loss column
    win_loss = []
    for _, row in phi_gm_stats.iterrows():

        # If the 76ers score more points, it's a win
        if row["teamPTS"] > row["opptPTS"]:
            win_loss.append("W")
        else:
            win_loss.append("L")

    # Add the win_loss data to the DataFrame
    phi_gm_stats["winLoss"] = win_loss

    gm_stats_cds = ColumnDataSource(phi_gm_stats)
    win_loss_mapper = CategoricalColorMapper(
        factors=["W", "L"], palette=["green", "red"]
    )

    # Create a dict with the stat name and its corresponding column in the data
    stat_names = {
        "Points": "teamPTS",
        "Assists": "teamAST",
        "Rebounds": "teamTRB",
        "Turnovers": "teamTO",
    }

    # The figure for each stat will be held in this dict
    stat_figs = {}

    # For each stat in the dict
    for stat_label, stat_col in stat_names.items():

        # Create a figure
        fig = figure(
            y_axis_label=stat_label,
            plot_height=200,
            plot_width=400,
            x_range=(1, 10),
            tools=["xpan", "reset", "save"],
        )

        # Configure vbar
        fig.vbar(
            x="game_num",
            top=stat_col,
            source=gm_stats_cds,
            width=0.9,
            color=dict(field="winLoss", transform=win_loss_mapper),
        )

        # Add the figure to stat_figs dict
        stat_figs[stat_label] = fig

    # Create layout
    grid = gridplot(
        [
            [stat_figs["Points"], stat_figs["Assists"]],
            [stat_figs["Rebounds"], stat_figs["Turnovers"]],
        ]
    )

    stat_figs["Points"].x_range = stat_figs["Assists"].x_range = stat_figs[
        "Rebounds"
    ].x_range = stat_figs["Turnovers"].x_range

    # Add a title for the entire visualization using Div
    html = """<h3>Philadelphia 76ers Game Log</h3>
    <b><i>2017-18 Regular Season</i>
    <br>
    </b><i>Wins in green, losses in red</i>
    """
    sup_title = Div(text=html)

    # Visualize
    st.bokeh_chart(column(sup_title, grid))
