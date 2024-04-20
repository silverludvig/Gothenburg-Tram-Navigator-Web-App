import sys
import csv
import numpy as np
import networkx as nx
from haversine import haversine
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

AIRPORTS_FILE = './data/airports.dat'
ROUTES_FILE = './data/routes.dat'

def mk_airportdict(AIRPORTS_FILE):
    airportdic = {}
    with open(AIRPORTS_FILE, 'r', encoding='utf-8') as csvfile:
        for line in csv.reader(csvfile):
            if line[6] != '\\N' and line[7] != '\\N':
                airportdic[line[0]] = {'Name': line[1], 'Country': line[3], 'IATA': line[4], 'posi': (float(line[6]), float(line[7]))}
    return airportdic

def mk_routeset(ROUTES_FILE):
    routeset = {}
    with open(ROUTES_FILE, 'r', encoding='utf-8') as csvfile:
        for line in csv.reader(csvfile):
            if line[3] != '\\N' and line[5] != '\\N':
                routeset.setdefault(line[3], []).append(line[5])
    return routeset

def mk_routegraph(routeset, airportdic):
    G = nx.Graph()
    for airport, data in airportdic.items():
        G.add_node(airport, posi=data['posi'])
    for start, destinations in routeset.items():
        for stop in destinations:
            if start in airportdic and stop in airportdic:
                dis = round(haversine(airportdic[start]['posi'], airportdic[stop]['posi']), 2)
                G.add_edge(start, stop, weight=dis)
    return G 



def plt_airport(G):
    positions = np.array([G.nodes[node]['posi'] for node in G.nodes])
    plt.figure(figsize=(16, 10))
    plt.scatter(positions[:, 1], positions[:, 0], s=5, alpha=0.7)
    plt.show()

def plt_route(G):
    positions = np.array([G.nodes[node]['posi'] for node in G.nodes])
    plt.figure(figsize=(16, 10))
    plt.scatter(positions[:, 1], positions[:, 0], s=5, alpha=0.7)

    for start, stop in G.edges:
        plt.plot(*zip(*[G.nodes[node]['posi'] for node in [start, stop]]), linewidth=0.3, alpha=0.8)
    plt.show()

def k_spanning_tree(G, k=1000):
    mst_edges = nx.minimum_spanning_edges(G, algorithm='kruskal', weight='weight', data=False)
    selected_edges = list(mst_edges)[-k:]

    positions = np.array([G.nodes[node]['posi'] for node in G.nodes])
    plt.figure(figsize=(16, 10))
    plt.scatter(positions[:, 1], positions[:, 0], s=5, alpha=0.7)

    for start, stop in selected_edges:
        plt.plot(*zip(*[G.nodes[node]['posi'] for node in [start, stop]]), linewidth=2, alpha=0.8)
    plt.show()

def k_means(posi_data, k=7):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(posi_data)
    labels = kmeans.labels_
    color_options = plt.cm.get_cmap('viridis', k)

    plt.figure(figsize=(16, 10))
    for label in range(k):
        idx = np.where(labels == label)[0]
        plt.scatter(posi_data[idx, 1], posi_data[idx, 0], s=2, alpha=0.7, color=color_options(label))
    plt.show()

if __name__ == '__main__':
    airportdic = mk_airportdict(AIRPORTS_FILE)
    routeset = mk_routeset(ROUTES_FILE)
    G = mk_routegraph(routeset, airportdic)

    command_parameters = sys.argv
    if len(command_parameters) > 1:
        action = command_parameters[1]
        if action == 'airports':
            plt_airport(G)
        elif action == 'routes':
            plt_route(G)
        elif action == 'span':
            k = int(command_parameters[2]) if len(command_parameters) > 2 else 1000
            k_spanning_tree(G, k)
        elif action == 'means':
            positions = np.array([[G.nodes[node]['posi'][0], G.nodes[node]['posi'][1]] for node in G.nodes])
            k = int(command_parameters[2]) if len(command_parameters) > 2 else 7
            k_means(positions, k)