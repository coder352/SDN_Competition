#!/usr/bin/python
# coding: utf-8

import random

class Node:
    def __init__(self, id = None, ip = None, type = 0):
        self.id = id
        self.ip = ip  # 包括 Host.ip 和 Switch.Id
        self.type = type  # 0 表示 Host, 1 表示 Switch

if __name__ == '__main__':
    node = Node(1, "10.1", 0)
    print node.id
    print node.ip
    print node.type

