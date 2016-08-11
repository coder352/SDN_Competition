#!/usr/bin/python
# coding: utf-8

import networkx as nx
from Topo import Topo
import matplotlib.pyplot as plt


class Network:

    def __init__(self):
        self.G = nx.Graph()

    def build(self, links):
        for i in range(0, len(links)):
            self.G.add_edge(links[i].fo, links[i].to)
        self.path = nx.all_pairs_shortest_path(self.G)

    def draw(self):
        nx.draw(self.G, with_labels=True, node_size=30)
        plt.show()

    def findPath(self, fo, to):
        print self.path[fo][to]

    def start(self):  # 供其它程序调用
        self.topo = Topo()
        self.topo.start()
        self.build(self.topo.links)


if __name__ == '__main__':
    topo = Topo()
    topo.start()
    network = Network()
    network.build(topo.links)
    network.findPath(12, 19)
    network.draw()
