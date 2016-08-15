#!/usr/bin/python
# coding: utf-8

import random


class Path:

    def __init__(self, path, time=0.5, flow=0):
        self.path = path
        self.time = time
        self.flow = random.random() * 0.1 + flow  # 流量

if __name__ == '__main__':
    path = [12, 11, 6, 8, 10, 5, 19]
    time = 0.6
    flow = 0.5
    link = Path(path, time, flow)
    print link.path
    print link.time
    print link.flow
