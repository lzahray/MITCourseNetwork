import networkx as nx
import pdb
import itertools
import numpy as np

import community



if __name__ == '__main__':
    G = nx.read_graphml("gephi-files/indegree-fixed.graphml")

    G_u = G.to_undirected()
    G_u.remove_nodes_from(list(nx.isolates(G_u)))
    
    print("Starting girvan newman")
    result = nx.algorithms.community.centrality.girvan_newman(G)

    first = tuple(c for c in next(result))

    pdb.set_trace()

    print("started takewhile")
    limited = itertools.takewhile(lambda c: len(c) <= 20 and len(c) > 10, result)
    print("finished takewhile")


    for communities in limited:
        pdb.set_trace()
        print(tuple(c for c in communities))
    pdb.set_trace()
   # result = nx.algorithms.community.asyn_fluidc(G_u, 25)
    result = nx.algorithms.community.label_propagation.label_propagation_communities(G_u)

    count = 0
    for c in result:
        print(c)
        count += 1
        
    print(count, " communities found.")
    pdb.set_trace()

    k_cliques = nx.algorithms.community.kclique.k_clique_communities(G_u, 2)

    
    for c in k_cliques:
        print(c)


    pdb.set_trace()


    k = 20


    pdb.set_trace()
