import networkx as nx
import pdb
import itertools
import numpy as np

import community


def kernighan(G):
    result = nx.algorithms.community.kernighan_lin.kernighan_lin_bisection(G)

    pdb.set_trace()

    


if __name__ == '__main__':
    G = nx.read_graphml("gephi-files/indegree-fixed.graphml")

    G_u = G.to_undirected()
    
    kernighan(G_u)

    pdb.set_trace()
