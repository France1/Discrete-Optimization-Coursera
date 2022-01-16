import numpy as np
import os
from collections import OrderedDict
from ortools.sat.python import cp_model


def parse_items(input_data):
    
    lines = input_data.strip().split('\n')
    items = []
    
    for i,line in enumerate(lines):
        line = line.split()
        if i==0: 
            #1st line is header
            num_nodes, num_edges = map(int, line)
        else:
            items.append(list(map(int, line)))

    return num_nodes, num_edges, items

def make_ordered_graph(items,num_nodes):

    g = {i:set() for i in range(num_nodes)}
    for u,v in items:
        g[u].add(v)
        g[v].add(u)

    # sort graph by valence of nodes
    g = OrderedDict(sorted(g.items(), key= lambda x: len(x[1]), reverse=True))

    return g

def algo_heuristic(g):
    # Welsh-Powell algorithm http://mrsleblancsmath.pbworks.com/w/file/fetch/46119304/vertex%20coloring%20algorithm.pdf

    colors = [None]*len(g)
    color = 0
    n_init, _ = g.popitem(last=False)
    colors[n_init] = color

    while None in colors:
        for u, nbrs in g.items():
            if colors[u] is None:
                nbrs_colors = [colors[v] for v in nbrs]
                if color not in nbrs_colors:
                    # print(f'assigned {color} to {u}')
                    colors[u] = color
        color += 1

    return colors

def algo_cp(items, num_nodes, target, time_limit=10):

    model = cp_model.CpModel()

    # Creates the variables.
    colors = [
        model.NewIntVar(0, num_nodes - 1, 'c%i' % i) for i in range(num_nodes)
    ]
    max_color = model.NewIntVar(0, num_nodes - 1 ,'obj')

    # Creates the constraints.
    for u,v in items:
        model.Add(colors[u] != colors[v])

    model.AddMaxEquality(max_color, colors)

    model.Add(colors[0] == 0)
    for i in range(num_nodes):
        model.Add(colors[i] <= i+1)

    # Minimize objective: model.Minimize(max_color) is too slow so we fix the 
    # target and solve for feasibility
    model.Add(max_color <= target)

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.Solve(model)

    # if solvers run over time limit return None
    try:
        results = [solver.Value(colors[i]) for i in range(num_nodes)]
    except IndexError:
        results = None

    return results

def solve_it(input_data):

    num_nodes, num_edges, items = parse_items(input_data)

    g = make_ordered_graph(items,num_nodes)
    colors = algo_heuristic(g)

    # iteratively improve the results until time limit is exceeded
    target = max(colors)
    while True:
        new_colors = algo_cp(items, num_nodes, target, time_limit=300)
        if new_colors is not None:
            colors = new_colors
            target -= 1
        else:
            break

    n_colors = max(colors)+1
    optimal_solution = 0

    return f'{n_colors} {optimal_solution}\n{" ".join(map(str, colors))}'


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

