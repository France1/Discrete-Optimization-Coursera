#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy.spatial import distance, KDTree, cKDTree
import math
import numpy as np


def parse_items(input_data):
    
    lines = input_data.strip().split('\n')
    items = []
    
    for i,line in enumerate(lines):
        line = line.split()
        if i==0: 
            #1st line is header
            num_nodes = int(line[0])
        else:
            items.append(tuple(map(float, line)))

    return num_nodes, items

def compute_objective(path, coords):

    path = path+[path[0]]
    obj = 0
    for start,end in zip(path[:-1],path[1:]):
        obj+=math.hypot(coords[end][0]-coords[start][0],coords[end][1]-coords[start][1])
    
    return obj

def tsp_nn(coords, num_nodes):

    # initialize
    coords = np.array(coords)
    nodes = list(range(num_nodes))
    visited = np.zeros(num_nodes,dtype=bool)
    tree = cKDTree(np.array(coords[nodes]))
    # startting node
    nearest = 0
    visited[nearest] = True
    path = [nearest]
    # visit nearest neighbours 
    while not visited.all():
        for k in range(2,num_nodes+1):
            dd, ii = tree.query(coords[nearest], k=k)
            # print(k, nearest, ii, dd, visited[ii])
            if not visited[ii].all():
                for n in ii:
                    if not visited[n]:
                        visited[n] = True
                        nearest = n
                        path += [nearest]
                        # print(f'>>>>> added {nearest} to path')
                        break
                break
    return path

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    num_nodes, coords = parse_items(input_data)
    path = tsp_nn(coords, num_nodes)
    obj = compute_objective(path,coords)

    return f'{obj} {0}\n{" ".join(map(str, path))}'


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

