#!/usr/bin/python
# coding: utf-8

from Link import Link
from Node import Node
import requests
import json


class Topo:
    hosts_url = "http://localhost:8080/wm/device/"  # 只会得到 Host 的数据 和 Host 所连接的主机
    switchs_url = "http://localhost:8080/wm/core/controller/switches/json"  # 得到 Switch 的数据
    links_switch_url = "http://localhost:8080/wm/topology/links/json"  # 只是 Switch 之间的 Link
    nodes = []
    links = []
    mapnodes = {}

    def __init__(self):
        print "hello"

    def getTopo(self):
        f = open("hosts")
        self.hosts = json.load(f)
        f = open("switchs")
        self.switchs = json.load(f)
        f = open("links_switch")
        self.links_switch = json.load(f)
        # 下面三行是在 mininet + floodlight 环境下获取拓扑信息,
        # 现在写死了, 拓扑信息获取后写入文件,然后用上面几行读出来
        # self.hosts = requests.get(self.hosts_url).json()
        # self.switchs = requests.get(self.switchs_url).json()
        # self.links_switch = requests.get(self.links_switch_url).json()

    def getSwitchs(self):
        self.len_switchs = len(self.switchs)
        for i in range(0, self.len_switchs):
            ip = str(self.switchs[i]['switchDPID'])
            self.nodes.append(Node(i, ip, 1))
            self.mapnodes[ip] = i

    def getHosts(self):  # 这里经常出错, 要执行 pingall
        self.len_hosts = len(self.hosts)
        for i in range(0, self.len_hosts):
            ip = str(self.hosts[i]['ipv4'][0])
            id = i + self.len_switchs
            self.nodes.append(Node(id, ip, 0))
            self.mapnodes[ip] = id
            # 顺便添加 Host - Switch 的链路
            to = self.mapnodes[str(self.hosts[i]["attachmentPoint"][0]["switchDPID"])]
            self.links.append(Link(id, to))

    def getLinks_Switch(self):  # 得到 Switchs 之间的链路
        self.len_links_switch = len(self.links_switch)
        for i in range(0, self.len_links_switch):
            to = self.mapnodes[str(self.links_switch[i]['dst-switch'])]
            fo = self.mapnodes[str(self.links_switch[i]['src-switch'])]
            self.links.append(Link(fo, to))

    def start(self):  # 按顺序执行前面的函数
        self.getTopo()
        self.getSwitchs()  # getSwitchs 和 getHosts 的调用顺序不能错
        self.getHosts()
        self.getLinks_Switch()

if __name__ == '__main__':
    topo = Topo()
    topo.getTopo()
    topo.getSwitchs()  # getSwitchs 和 getHosts 的调用顺序不能错
    # print json.dumps(topo.switchs, indent = 1)
    topo.getHosts()
    # print json.dumps(topo.hosts, indent = 1)
    topo.getLinks_Switch()
    # print json.dumps(topo.links_switch, indent = 1)

    # 测试 Nodes
    # for i in range(0, len(topo.nodes)):
        # print topo.mapnodes[topo.nodes[i].ip]
        # print topo.nodes[i].ip
        # print topo.nodes[i].type

    # 测试 Links
    # for i in range(0, len(topo.links)):
        # print topo.links[i].fo,
        # print topo.links[i].to
        # print topo.links[i].bw
        # print topo.nodes[topo.links[i].fo].ip
        # print topo.nodes[topo.links[i].to].ip
    # print
    # for i in range(0, len(topo.links)):
        # print topo.nodes[topo.links[i].fo].ip
