import networkx as nx
import pdb
import itertools
import numpy as np

import community

def louvain(G):

    for x in np.logspace(-4, 2, 7):
        result = community.best_partition(G, resolution=x)
        np.save("comm-data/louvain-"+str(x)+".npy", np.asarray(result))


if __name__ == '__main__':
    G = nx.read_graphml("gephi-files/indegree-fixed.graphml")

    pdb.set_trace()

    G_u = G.to_undirected()
    
    louvain(G_u)

