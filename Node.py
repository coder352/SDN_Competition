#!/usr/bin/python
# coding: utf-8
import random
class Node:
    def __init__(self, id=None, ip=None, type=0, name=None):
        self.id = id
        self.ip = ip  # 包括 Host.ip 和 Switch.Id
        self.type = type  # 0 表示 Host, 1 表示 Switch
        self.name = name
    def __str__(self):
        return 'id: ' + str(self.id) + '; ip: ' + self.ip + '; type: ' + ['Host', 'Switch'][self.type] + '; name: ' + self.name
    __repr__ = __str__
if __name__ == '__main__':
    node = Node(1, "10.1", 0, 'H1')
    print(node)
    print(node.__dict__)
