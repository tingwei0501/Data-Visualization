# -*- coding: utf-8 -*-
import random
from bokeh.plotting import figure, curdoc
"""
@author: Lucy
HW3a
"""

file = open('test1.txt', 'r')
count = 0
G = {}
GWMIN = set()
first = True
total_weight = 0

################################################
""" handle data input """
for line in file:
    line = line.split()
    
    if count == 0:
        node_num = int(line[0])
    if count == 1:
        for i in range(0, node_num):
            G[i] = {int(line[i]):[]}
    elif count > 1 and count <= (node_num+1):
        for i in range(0, node_num):
            # not integer, str #
            if line[i] == '1':
                keys = G[count-2].keys()
                # get weight of node #
                for k in keys:
                    key = k
                G[count-2][key].append(i)
    count = count + 1

check = [0]*node_num
################################################
p1 = figure(toolbar_location=None)
cir = p1.circle(x=[], y=[], size=30)
dc = cir.data_source

""" compute GWMIN """
def compute():
    global first, GWMIN, G, check
    y = []
    if first:
        ### initial set ###
        for i in range(0, node_num):
            if (random.randint(0, 1)):
                GWMIN.add(i)
                keys = G[i].keys()
                for k in keys:
                    weight = k
        first = False

    num = 0
    node = random.randint(0,node_num-1)
    keys = G[node].keys()
    for k in keys:
        weight = k
    degree = len(G[node][weight])
    node_value = weight/(degree+1)
    for i in G[node][weight]:
        keys = G[i].keys()
        for k in keys:
            neighbor_weight = k
        neighbor_degree = len(G[i][neighbor_weight])
        neighbor_value = neighbor_weight/(neighbor_degree+1)
        if neighbor_value < node_value:
            num = num + 1
        elif (i in GWMIN) == False:
            num = num + 1
        else:
            continue
        
    # I join #
    if num == degree:
        # not change decission #
        if node in GWMIN:
            # set flag to 1 #
            check[node] = 1
        else:
            GWMIN.add(node)
            check = [0]*node_num
    # not join #
    else:
        # not change decission #
        if node not in GWMIN:
            check[node] = 1
        else:
            check = [0]*node_num
            GWMIN.remove(node)

    for i in range(node_num):
        if i in GWMIN:
            y.append(1)
        else:
            y.append(0)

    new_data = dict()
    new_data['x'] = [i for i in range(node_num)]
    new_data['y'] = y
    dc.data = new_data

curdoc().add_periodic_callback(compute, 100)
    
curdoc().add_root(p1)