#!/usr/bin/python
# coding: utf-8

import random


class Link:

    def __init__(self, fo=0, to=0):
        self.fo = fo  # 链路的起点
        self.to = to  # 链路的终点
        self.bw = random.random() * 100 + 1000  # 带宽
        self.ec = random.random() * 100 + 1000  # 能耗


if __name__ == '__main__':
    link = Link(1, 2)
    print link.fo
    print link.bw
    print link.ec
