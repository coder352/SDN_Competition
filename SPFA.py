#!/usr/bin/python
# coding: utf-8

global n, m, k, edge, head, dis, stack, vis, nMax, mMax, inf
nMax = 100
mMax = 10000
inf = 1e+10


class e(object):
    pass
n = 0
k = 0
m = 0
eg = e()
edge = []
head = [0]
dis = [0]
stack = [0]
vis = [0]


def addedge(a, b, c):
    global k, edge, head
    ed = e()
    ed.u = a  # you can delect it
    ed.v = b
    ed.w = c
    ed.next = head[a]
    edge.append(ed)
    head[a] = k
    k += 1
    pass


def spfa():
    global n, m, k, edge, head, dis, stack, vis, inf
    i = top = 0
    for i in range(0, n):
        dis[i] = inf
        vis[i] = 0
    dis[0] = 0
    vis[0] = 1
    top += 1
    stack[top] = 0
    while(top != 0):
        u = stack[top]
        top -= 1
        i = head[u]
        while(i != 0):
            v = edge[i].v
            if dis[v] > dis[u] + edge[i].w:
                dis[v] = dis[u] + edge[i].w
                if(vis[v] == 0):
                    vis[v] = 1
                    top += 1
                    stack[top] = v
            i = edge[i].next
        vis[u] = 0
    pass

if __name__ == '__main__':
    u = v = l = i = 0
    for i in range(0, nMax):
        head.append(0)
        dis.append(0)
        vis.append(0)
        stack.append(0)
    while(1):
        na = input()
        n = int(na)
        ma = input()
        m = int(ma)
        edge = [0]
        k = 1
        for i in range(0, n):
            head[i] = 0
        for i in range(0, m):
            ua = input()
            va = input()
            la = input()
            u = int(ua)
            v = int(va)
            l = int(la)
            addedge(u, v, l)
        spfa()
        for i in range(1, n):
            print(dis[i])
