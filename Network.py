#!/usr/bin/python
# coding: utf-8
# 1. [Graph – Undirected graphs with self loops](https://networkx.readthedocs.io/en/stable/reference/classes.graph.html)
# 2. [Reference](https://networkx.readthedocs.io/en/stable/reference/index.html)
import networkx as nx
from Topo import Topo
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread, Condition
import random
condition = Condition()  # 工厂方法, 能让一个或多个线程 wait
class Path(Thread):
    """Simulate a path

    这个类的作用只是在 Network 中模拟一个路径
    Path(path, time, flow).start() 只在这里用到过

    Attributes:
        path_dic: Network 传递过来的成员变量, 存储所有 paths, path_dic[self.key] = self.path. Format as below:
            {'H1H5': ['H1', 'S9', 'S5', 'S1', 'S7', 'S11', 'H5']}
        G: Network 传递过来的成成员变量, nx.graph()
        path_flow_dic: Network 传递过来的成成员变量, path_flow_dic[str(self.path)] = self.flow. Format as below:
            {"['H1', 'S9', 'S5', 'S1', 'S7', 'S11', 'H5']": 3.0618346296413868}.
        以上三个变量是公用变量, 相当于全局变量, 修改要加锁

        path: 路径的表示. Format as below:
            ['H1', 'S9', 'S5', 'S1', 'S7', 'S11', 'H5']
        time: current path 的存在时间, 表示这段时间这部分带宽(flow)一直被这个 path 占用
        flow: current path 上的流量带宽, 是一个 float 值, 加上了一部分的随机性
        key: 将 path 的首尾取出作为其索引值. For example: H1H5

    Functions:
        run(): 重写 Thread 类的方法实现多线程, 包含四部分操作全局性变量 G, path_dic, path_flow_dic 的代码
            都用 Condition 锁住了
    """
    def __init__(self, G, path_dic, path_flow_dic, path, time=0.5, flow=0):
        Thread.__init__(self)
        self.G, self.path_dic, self.path_flow_dic = G, path_dic, path_flow_dic
        self.path, self.time = path, time
        self.flow = random.random() * 0.1 + flow  # 流量
        self.key = path[0] + path[-1]
    def run(self):
        condition.acquire()  # 请求一个锁, 操作 Network 的成员变量, 相当于是全局变量
        self.path_dic[self.key] = self.path
        self.path_flow_dic[str(self.path)] = self.flow
        condition.notify()  # 唤醒一个在这个 condition 上阻塞的进程
        condition.release()  # 执行完以后，释放锁

        condition.acquire()
        for i in range(len(self.path) - 1):  # 将 path 中对应的边的权重增加
            self.G.edge[self.path[i]][self.path[i + 1]]['weight'] += self.flow
            self.G.edge[self.path[i + 1]][self.path[i]]['weight'] += self.flow
        condition.notify()
        condition.release()

        sleep(self.time)  # 在这段时间里, 这里的部分带宽一直被这个 path 占着

        condition.acquire()
        for i in range(len(self.path) - 1):
            self.G.edge[self.path[i]][self.path[i + 1]]['weight'] -= self.flow
            self.G.edge[self.path[i + 1]][self.path[i]]['weight'] -= self.flow
        condition.notify()
        condition.release()

        condition.acquire()
        del self.path_dic[self.key]
        del self.path_flow_dic[str(self.path)]
        condition.notify()
        condition.release()

class Network:
    """Achieve the function of normal network

    Longer class information

    Attributes:
        G: nx.graph()
        topo: Reference to ./Topo.py
        path_dic: 存储所有 paths, key 是起始节点和终止节点, path_dic[self.key] = self.path. Format as below:
            {'H1H5': ['H1', 'S9', 'S5', 'S1', 'S7', 'S11', 'H5']}
        path_flow_dic: 每条路径的流量, path_flow_dic[str(self.path)] = self.flow. Format as below:
            {"['H1', 'S9', 'S5', 'S1', 'S7', 'S11', 'H5']": 3.0618346296413868}.
        unweighted_shortest_path_dic: 在刚搭建好 G 的时候就开始计算各个节点之间的最短路径

    Functions:
        build(): 用 Topo.links 搭建好计算, 顺便计算没有权重的所有路径. Variable format as:
            link: Obj( from: 19; to: 11; bandwidth: 1055.8915955672046; energy_cost: 1065.1928101438953 )
            node: Obj( id: 19; ip: 10.0.0.8; type: Host; name: H8 )
        findNormalPath(fo, to): 根据 build() 函数中的计算结果 unweighted_shortest_path_dic 来查找路径, 返回 list
        findPathbyWeight(fo, to, time=1, flow=3): 查找以 fo + to 为键值的加权路径是否存在, 没有就有 dijkstra_path 算法新建,
            这里也是 path_dic 变量逐步完善的地方
    """
    def __init__(self):
        self.G, self.topo = nx.Graph(), Topo()
        self.path_dic, self.path_flow_dic = {}, {}
        self.unweighted_shortest_path_dic = {}
    def build(self):
        for link in self.topo.links:
            self.G.add_edge(self.topo.nodes[link.fo].name, self.topo.nodes[link.to].name, weight=1, capacity=0, length=100)
            # 以字符串为节点名称, 三种权重模式, capcity 初始化为0, 每次查询增加 1
        self.unweighted_shortest_path_dic = nx.all_pairs_shortest_path(self.G)  # 先找没有权重的路径
    def findNormalPath(self, fo, to):
        return self.unweighted_shortest_path_dic[fo][to]
    def findPathbyWeight(self, fo, to, time=1, flow=3):
        key = fo + to
        if key not in self.path_dic:
            path = nx.dijkstra_path(self.G, fo, to, weight='weight')
            Path(self.G, self.path_dic, self.path_flow_dic, path, time, flow).start()  # sleep 5s, 消耗一个带宽
        else:
            path = self.path_dic[key]
        return path
    def findPathbyCapacity(self, fo, to):  # 这里还没写好, 暂时还是用的 weight
        path = nx.dijkstra_path(self.G, fo, to, weight='capacity')
        return path
    def findPathbyLength(self, fo, to):
        path = nx.dijkstra_path(self.G, fo, to, weight='length')
        return path
    def drawTopo(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_size=500)
        plt.show()
    def drawFlow(self):
        num = []
        for i in range(15):
            num.append(0)
        for path in self.path_dic.values():
            for i in range(1, len(path) - 1):
                num[int(path[i].strip('S'))] += self.path_flow_dic[str(path)]
        x = list(range(0, 15))
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
        self.topo.start()
        self.build()
if __name__ == '__main__':
    network = Network()
    # path = ['hello', 11, 6, 8, 10, 5, 'jrp']
    # time = 6
    # flow = 0.5
    # link = Path(network.G, network.path_dic, network.path_flow_dic, path, time, flow)
    # print(link.path_flow_dic)
    # print(link.path)
    # print(link.time)
    # print(link.flow)
    # print(link.key)

    network.start()
    # print network.findNormalPath('H1', 'H5')
    # ['H1', 'S9', 'S6', 'S3', 'S8', 'S11', 'H5']
    # print network.findNormalPath('H1', 'H5')
    # network.G.edge['S9']['S6']['weight'] = 8
    # network.G.edge['S9']['S5']['weight'] = 0.5  # weight 越小,选中的几率越大
    print(network.findPathbyWeight('H1', 'H5', 6, 4))
    print(network.findPathbyWeight('H2', 'H6'))
    print(network.findPathbyWeight('H4', 'H7'))
    network.drawFlow()

    # 测试权重
    # network.G.edge['H1']['S9']['weight'] = 7
    # # print network.G.edges(data=True)  # 多个属性都会输出来
    # print network.G.edges(data='weight')  # 只会输出来weight的属性
    # print network.G.edge['H1']['S9']['weight']
