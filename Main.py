#!/usr/bin/python3
# coding: utf-8
from Network import Network
network = Network()
# path = ['hello', 11, 6, 8, 10, 5, 'jrp']
# time = 6
# flow = 0.5
# link = Path(network.G, network.paths, network.pathsflow, path, time, flow)
# print(link.pathsflow)
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
