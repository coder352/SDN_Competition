#!/usr/bin/python
# coding: utf-8
import random
class Link:
    def __init__(self, fo=0, to=0, bw=random.random() * 100 + 1000, ec=random.random() * 100 + 1000):
        self.fo = fo  # 链路的起点
        self.to = to  # 链路的终点
        self.bw = bw  # 带宽
        self.ec = ec  # 能耗
    def __str__(self):
        return 'from: ' + str(self.fo) + '; to: ' + str(self.to) + '; bandwidth: ' + str(self.bw) + '; energy_cost: ' + str(self.ec)
if __name__ == '__main__':
    link = Link(1, 2)
    print(link)
    print(link.__dict__)
