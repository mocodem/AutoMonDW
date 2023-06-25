import oniondb
import pandas as pd
import networkx as nx
from pyvis.network import Network
import json
import matplotlib.pyplot as plt
import uuid

# Load seeds from JSON file
with open("sources/seeds.json", "r") as f:
    seeds = json.loads(f.read())["directories"]

# Create an empty DataFrame
data = {'sources': [], 'onions': []}
df = pd.DataFrame(data)

# Get all v3 onions with their sources
all_onions = oniondb.get_all_onions_v3_source()
all_good = oniondb.get_all_onions_status(200)

# Populate the DataFrame with source-onion pairs
for (onion, source) in all_onions:
    if "http://torlinks.net" in source:
        source = "http://torlinks.net"
    onion = "live_onion_" + onion[:10] + onion[-10:] if onion in all_good else "bad_onion_" + onion[:10] + onion[-10:]
    df.loc[len(df.index)] = [source, onion]

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, source='sources', target='onions')
d = nx.degree(G)
d = list(d)

# Print degree information for nodes in seeds
for i in d:
    if i[0] in seeds:
        print(i)

input()

# Create a network visualization using pyvis
N = Network(directed=True)
N.repulsion()

# Add nodes to the network visualization
for i, node in enumerate(G):
    if node in seeds or "http://torlinks.net" in node:
        color = "#8e2db8"
        size = d[i][1]
        label = node
    elif "live_onion_" in node:
        color = "#f389ca"
        size = 5 * d[i][1]
        label = "live onion"
    else:
        color = "#808080"
        size = 5 * d[i][1]
        label = "dead onion"

    N.add_node(node, label=label, color=color, size=size)

# Add edges to the network visualization
for e in G.edges:
    N.add_edge(e[0], e[1])

# Write the network visualization to an HTML file
N.write_html('graph.html')
