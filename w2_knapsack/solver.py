#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])

def parse_items(input_data):
    
    lines = input_data.strip().split('\n')
    items = []
    
    for i,line in enumerate(lines):
        line = line.split()
        if i==0: 
            #1st line is header
            item_count, capacity = map(int, line)
        else:
            items.append(Item(i-1, int(line[0]), int(line[1])))

    return item_count, capacity, items

def algo_heuristic(items,capacity):

    weight, value = 0,0
    taken = [0]*len(items) 

    # sort item by descending value density
    for item in sorted(items, key = lambda x: x.value/x.weight, reverse=True):
        # add item until capacity is reached        
        if weight+item.weight <= capacity:
            weight += item.weight
            value += item.value
            taken[item.index] = 1

    return value, taken

def algo_dp(items,capacity):
    
    # 1. Initialize table
    N = len(items)
    M = [[0 for _ in range(N+1)] for _ in range(capacity+1) ]
    # 2. Fill table and get value
    for i in range(1,N+1):
        v_i = items[i-1].value
        w_i = items[i-1].weight
        for k in range(capacity+1):
            if k<w_i:
                M[k][i] = M[k][i-1]
            else:
                M[k][i] = max(M[k][i-1], v_i+M[k-w_i][i-1])
    value = M[-1][-1]
    # 3. Trace back items
    taken = []
    for i in reversed(range(1,N+1)):
        w_i = items[i-1].weight
        if M[k][i]==M[k][i-1]:
            taken.insert(0,0)
        else:
            k = k-w_i
            taken.insert(0,1)
    
    return value, taken

def solve_it(input_data):

    item_count, capacity, items = parse_items(input_data)
    if (item_count<=1.e3) and (capacity<3.e6):
        optimal_solution = 0
        value, taken = algo_dp(items,capacity)
    else:
        optimal_solution = 1
        value, taken = algo_heuristic(items,capacity)
    
    return f'{value} {optimal_solution}\n{" ".join(map(str, taken))}'


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

