#!/usr/bin/python
# coding: utf-8
"""Store topo in two variables nodes and links"""
from Link import Link
from Node import Node
import requests, json
HOSTS_URL = "http://localhost:8080/wm/device/"                           # 只会得到 host 的数据 和 host 所连接的主机
SWITCHES_URL = "http://localhost:8080/wm/core/controller/switches/json"  # 得到 switch 的数据
LINKS_SWITCH_URL = "http://localhost:8080/wm/topology/links/json"        # 只是 switch 之间的 link
class Topo:
    """Build a topo

    Based on class Node and Link, get information of topo as three variables: hosts,
    switches, links_switch from file or SND Controller API.
    Then build a topo with two elements of nodes and links.

    Attributes:
        hosts, switches, links_switch: Get date from .json file or Controller API. Format as below:
            host        : { "mac": ["00:00:00:00:00:01"], "ipv4": ["10.0.0.1"], "attachmentPoint": [{"switchDPID": "00:00:00:00:00:00:00:09", "port": 3, "errorStatus": null}]}
            switch      : { "switchDPID": "00:00:00:00:00:00:00:03" }
            link_switch : { "src-switch": "00:00:00:00:00:00:00:06", "src-port": 4, "dst-switch": "00:00:00:00:00:00:00:0a", "dst-port": 2 }
        nodes, links: Build a topo with elements of nodes and links, generated from getHosts(), getSwitches() and getLinks_switch(). Fromat as below:
            node: Obj( id: 19; ip: 10.0.0.8; type: Host; name: H8 )
            link: Obj( from: 19; to: 11; bandwidth: 1055.8915955672046; energy_cost: 1065.1928101438953 )
        ip_id_dic: A anti-check of nodes, it can use key of id to find a Node object. Format as below:
            {'00:00:00:00:00:00:00:01': 0, '00:00:00:00:00:00:00:02': 1}

    Functions:
        getTopo()                  : Get the three variables(hosts, switches, links_switch) from file or Controller API.
        getHosts() & getSwitches() : Store the hosts and switches of the topo as variable nodes.
        getLinks_switch()          : Store the links between switches as variable links
        sort_all()                 : 对 nodes 和 hosts 进行排序, 方便以后使用, hosts, switches, links_switch 的排序在读入的时候就完成了, 因为他们会影响到 getHosts() 和 getSwitches().
        start()                    : The functions above need to run in oredr, so I write a function to order them.
    """
    def __init__(self):
        self.hosts, self.switches, self.links_switch = [], [], []  # 从文件中获取
        self.nodes, self.links = [], []  # 从上面三个变量中分析出来
        self.ip_id_dic = {}  # 将 IP/switchDPID -> id
    def __str__(self):
        for link in self.links: res.append((self.nodes[link.fo].name, self.nodes[link.to].name))
        return str([(self.nodes[link.fo].name, self.nodes[link.to].name) for link in self.links])
    __repr__ = __str__
    def getTopo(self):
        f = open("hosts.json")
        self.hosts = json.load(f)
        self.hosts = sorted(self.hosts, key=lambda x: x['ipv4'])
        f = open("switches.json")
        self.switches = json.load(f)
        self.switches = sorted(self.switches, key=lambda x: x['switchDPID'])
        f = open("links_switch.json")
        self.links_switch = json.load(f)
        self.links_switch = sorted(self.links_switch, key=lambda x: x['src-switch'])
        # 下面三行是在 mininet + floodlight 环境下获取拓扑信息, 现在写死了, 拓扑信息获取后写入文件, 然后用上面几行读出来
        # self.hosts = requests.get(HOSTS_URL).json()
        # self.switches = requests.get(SWITCHES_URL).json()
        # self.links_switch = requests.get(LINKS_SWITCH_URL).json()
    def getSwitches(self):
        self.len_switches = len(self.switches)
        for i in range(0, self.len_switches):
            ip = str(self.switches[i]['switchDPID'])
            self.nodes.append(Node(i, ip, 1, 'S' + str(i + 1)))  # __init__(self, id=None, ip=None, type=0, name=None), 编号从 0-11, 12- 是 host
            self.ip_id_dic[ip] = i
    def getHosts(self):  # 这里经常出错, 要执行 pingall
        self.len_hosts = len(self.hosts)
        for i in range(0, self.len_hosts):
            ip = str(self.hosts[i]['ipv4'][0])
            id = i + self.len_switches
            self.nodes.append(Node(id, ip, 0, 'H' + str(i + 1)))  # H1 对应着 12, H8 对应着 19
            self.ip_id_dic[ip] = id
            # 顺便添加 Host - Switch 的链路
            to = self.ip_id_dic[
                str(self.hosts[i]["attachmentPoint"][0]["switchDPID"])]
            self.links.append(Link(id, to))  # 对应着 0 - 19 的数字
    def getLinks_Switch(self):  # 得到 Switches 之间的链路
        self.len_links_switch = len(self.links_switch)
        for i in range(0, self.len_links_switch):
            to = self.ip_id_dic[str(self.links_switch[i]['dst-switch'])]
            fo = self.ip_id_dic[str(self.links_switch[i]['src-switch'])]
            self.links.append(Link(fo, to))  # 对应着 0 - 19 的数字, 12 台 Switches, 8 台 Hosts
    def sort_all(self):
        self.nodes = sorted(self.nodes, key=lambda x: x.ip)
        self.links = sorted(self.links, key=lambda x: x.fo)
    def start(self):  # 按顺序执行前面的函数
        self.getTopo()
        self.getSwitches()  # getSwitches 和 getHosts 的调用顺序不能错
        self.getHosts()
        self.getLinks_Switch()
        self.sort_all()
if __name__ == '__main__':
    topo = Topo()
    topo.start()
    # print(json.dumps(topo.switches, indent = 1))
    # print(json.dumps(topo.hosts, indent = 1))
    # print(json.dumps(topo.links_switch, indent = 1))

    # test ip_id_dic
    print(topo.ip_id_dic)

    # test nodes
    print(topo.nodes)
    for node in topo.nodes:  # nodes include switch and host
        print(node)
        print(node.ip, node.type, node.name, end=' ')
        # switchDPID and IP; 1 means switch, 0 means host; S1-12, H1-8
        print(topo.ip_id_dic[node.ip])  # 0-19
        # print(topo.nodes[i].id, end=' ')  # 0-19

    # test links
    print(topo.links)
    for link in topo.links:
        print(link)
        print(link.fo, link.to, link.bw)
        print(topo.nodes[link.fo].name, end=' ')
        print(topo.nodes[link.to].name, end=' ')
        print(topo.nodes[link.fo].ip, end=' ')
        print(topo.nodes[link.to].ip)

    # test __str__, __repr__
    print(topo)
