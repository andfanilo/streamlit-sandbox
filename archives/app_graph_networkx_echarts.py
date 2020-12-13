import networkx as nx
import streamlit as st
from streamlit_echarts import st_echartsst.title("Hello world")G = nx.read_gexf("./data/ForFanilo.gexf")data = nx.node_link_data(G)def transform_node(node):
    node["name"] = node.pop("label")
    return nodedef transform_link(link):
    return linknodes = [transform_node(n) for n in data["nodes"]]
links = [transform_link(l) for l in data["links"]]option = {
    "title": {
        "text": 'FOOTBALL',
        "subtext": 'Default layout',
        "top": 'bottom',
        "left": 'right'
    },
    "tooltip": {},
    "series": [{
        "name": "FOOTBALL",
        "type": "graph",
        "layout": "force",
        "data": nodes,
        "links": links,
        "roam": True,
        "symbolSize": 20,
        "label": {
            "position": 'right'
        },
        "force": {
            "repulsion": 100
        }
    }]
}
st_echarts(option)