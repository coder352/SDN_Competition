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
        self.normal_path = nx.all_pairs_shortest_path(self.G)  # 先找好权值为 1 的路径

    def draw(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_size=500)
        plt.show()

    def findNormalPath(self, fo, to):
        return self.normal_path[fo][to]

    # def findPath(self, fo, to):
        # # path = nx.shortest_path(self.G, fo, to, 0.3)
        # # print type(path)
        # return nx.shortest_path(self.G, fo, to, 0.3)
        # pass

    # def calcWeight(self):
        # pass

    def start(self):
        self.topo = Topo()
        self.topo.start()
        self.build(self.topo.links)



if __name__ == '__main__':
    network = Network()
    network.start()

    print network.findNormalPath(12, 19)
    print network.findPath(12, 19)
    network.draw()
