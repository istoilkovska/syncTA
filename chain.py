import os
import sys
import importlib
import re

def compute_sub(guard_str):
    parens = []
    sub = []
    for i in range(len(guard_str)):        
        if guard_str[i] == '(':
            parens.append(i)
        if guard_str[i] == ')':
            j = parens.pop()
            g = guard_str[j:i + 1].strip()
            if g.startswith('(+') or g.startswith('(-') or g.startswith('(*'):
                continue            
            sub.append(g)
    return sub


def compute_atomic(guards):
    atomic = []
    for g in guards:
        a = []
        if str(g).startswith('(and ') or str(g).startswith('(not '):
            a = compute_sub(g[4:-1])            
        elif str(g).startswith('(or '):
            a = compute_sub(g[4:-1])
        else:
            if g not in atomic and g != 'true':
                atomic.append(g)                
        for x in a:
            guards.append(x)

    return atomic

def compute_graph(local, rules):
    # remove self-loops, obtain a dag
    graph = {}
    for l in local:
        graph[l] = [r['to'] for r in rules if r['from'] == l and r['to'] != r['from']]
    return graph

def dfs(graph, vertex, explored=None, path=None):
    if explored == None:
        explored = []
    if path == None:
        path = [vertex]

    explored.append(vertex)

    paths = []
    for w in graph[vertex]:
        if w not in explored:
            new_path = path + [w]
            paths.append(new_path)
            paths.extend(dfs(graph, w, explored[:], new_path))

    return paths

def longest_path(graph, initial):
    max_len = 0
    for i in initial:
        paths = dfs(graph, i)
        max_i = max([len(p) - 1 for p in paths])
        if max_len < max_i:
            max_len = max_i
    return max_len

def compute_bound(algorithm, pkg):

    alg = importlib.import_module("." + algorithm, package=pkg)

    guards = [r['guard'] for r in alg.rules]
    atomic = compute_atomic(guards)
    Psi = len(atomic)
    graph = compute_graph(alg.local, alg.rules)
    c = longest_path(graph, alg.initial)

    return (Psi, c)


if __name__ == "__main__":
    pass