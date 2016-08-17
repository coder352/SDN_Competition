#!/usr/bin/python
# coding: utf-8
# 参考
# 1. Graph – Undirected graphs with self loops
# https://networkx.readthedocs.io/en/stable/reference/classes.graph.html
# 2. Reference
# https://networkx.readthedocs.io/en/stable/reference/index.html

import networkx as nx
from Topo import Topo
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread, Condition
import random
condition = Condition()  # 工厂方法，能让一个或多个线程wait


class Path(Thread):

    def __init__(self, path, time=0.5, flow=0):
        Thread.__init__(self)
        global paths
        global G
        self.path = path
        self.time = time
        self.flow = random.random() * 0.1 + flow  # 流量
        self.key = path[0] + path[len(path) - 1]

    def run(self):
        condition.acquire()  # 请求一个锁
        paths[self.key] = self.path
        pathsflow[str(self.path)] = self.flow
        condition.notify()  # 唤醒一个在这个condition上阻塞的进程
        condition.release()  # 执行完以后，释放锁
        # print paths

        for i in range(len(self.path) - 1):  # 将 path 中对应的边的权重增加
            condition.acquire()  # 请求一个锁
            G.edge[self.path[i]][self.path[i + 1]]['weight'] += self.flow
            G.edge[self.path[i + 1]][self.path[i]]['weight'] += self.flow
            condition.notify()  # 唤醒一个在这个condition上阻塞的进程
            condition.release()  # 执行完以后，释放锁

        sleep(self.time)  # 在这段时间里,这里的部分带宽一直被这个path占着

        for i in range(len(self.path) - 1):
            condition.acquire()  # 请求一个锁
            G.edge[self.path[i]][self.path[i + 1]]['weight'] -= self.flow
            G.edge[self.path[i + 1]][self.path[i]]['weight'] -= self.flow
            condition.notify()  # 唤醒一个在这个condition上阻塞的进程
            condition.release()  # 执行完以后，释放锁

        condition.acquire()  # 请求一个锁
        del paths[self.key]
        del pathsflow[str(self.path)]
        condition.notify()  # 唤醒一个在这个condition上阻塞的进程
        condition.release()  # 执行完以后，释放锁
        # print paths

# if __name__ == '__main__':
#     path = ['hello', 11, 6, 8, 10, 5, 'jrp']
#     time = 0.6
#     flow = 0.5
#     link = Path(path, time, flow)
#     print link.path
#     print link.time
#     print link.flow
#     print link.key
#     print


class Network:

    def __init__(self):
        global paths
        global G
        global pathsflow
        paths = {}  # 存放 起始节点 和 终止节点的dict, example: 'H1H2': "{'H1', 'S1', 'S2', 'S3', 'H2'}"
        pathsflow = {}  # 存放每条路径的流量
        G = nx.Graph()

    def build(self, links):
        for i in range(0, len(links)):
            G.add_edge(Topo.nodes[links[i].fo].name, Topo.nodes[
                links[i].to].name, weight=1, capacity=0,
                length=100)
            # 以字符串为节点名称, 三种权重模式, capcity 初始化为0, 每次查询增加 1
        self.normal_path = nx.all_pairs_shortest_path(G)  # 先找好权值为 1 的路径

    def findNormalPath(self, fo, to):
        return self.normal_path[fo][to]

    def findPathbyWeight(self, fo, to, time=1, flow=3):
        key = fo + to
        if key not in paths:
            path = nx.dijkstra_path(G, fo, to, weight='weight')
            Path(path, time, flow).start()  # sleep 5s, 消耗一个带宽
        else:
            path = self.paths[key]
        return path

    def findPathbyCapacity(self, fo, to):  # 这里还没写好, 暂时还是用的 weight
        path = nx.dijkstra_path(G, fo, to, weight='capacity')
        return path

    def findPathbyLength(self, fo, to):
        path = nx.dijkstra_path(G, fo, to, weight='length')
        return path

    def drawTopo(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_size=500)
        plt.show()

    def drawFlow(self):
        num = []
        for i in range(15):
            num.append(0)
        for path in paths.itervalues():
            for i in range(1, len(path) - 1):
                num[int(path[i].strip('S'))] += pathsflow[str(path)]
        x = range(0, 15)
        plt.plot(x, num, color='r')
        plt.bar(x, num, alpha=.5, color='g')
        plt.xlim(0, 15)
        plt.ylim(0, 80)
        plt.title("flow analyse")
        plt.xlabel('Switchs')
        plt.ylabel('Flows')
        plt.show()
        # plt.savefig("./static/images/flow.png")

    def drawEnergy(self):
        pass

    def start(self):
        self.topo = Topo()
        self.topo.start()
        self.build(self.topo.links)


if __name__ == '__main__':
    network = Network()
    network.start()
    # print network.findNormalPath('H1', 'H5')
    # ['H1', 'S9', 'S6', 'S3', 'S8', 'S11', 'H5']
    # print network.findNormalPath('H1', 'H5')
    # network.G.edge['S9']['S6']['weight'] = 8
    # network.G.edge['S9']['S5']['weight'] = 0.5  # weight 越小,选中的几率越大
    print network.findPathbyWeight('H1', 'H5')
    print network.findPathbyWeight('H2', 'H6')
    print network.findPathbyWeight('H4', 'H7')
    network.drawFlow()

    # 测试权重
    # network.G.edge['H1']['S9']['weight'] = 7
    # # print network.G.edges(data=True)  # 多个属性都会输出来
    # print network.G.edges(data='weight')  # 只会输出来weight的属性
    # print network.G.edge['H1']['S9']['weight']
