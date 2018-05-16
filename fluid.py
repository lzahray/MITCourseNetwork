import networkx as nx
import pdb
import itertools
import numpy as np

import community



if __name__ == '__main__':
    G = nx.read_graphml("outdegreeGIRsGrouped.graphml")


    G_u = G.to_undirected()

    G_u.remove_nodes_from(list(nx.isolates(G_u)))
    
    # get connected components
    for cc in nx.connected_component_subgraphs(G_u):
        print(len(cc.nodes()))
        size = len(cc.nodes())
        num_comm = round(size / 100.0)
        result = nx.algorithms.community.asyn_fluidc(cc, max(1, num_comm))

        out_dict = {}

        for i, r in enumerate(result):
            for c in r:
                G.add_node(c, fluid_comm = i)
                out_dict[c] = i

        np.save("comm-data/fluid.npy", np.asarray(out_dict))


    nx.write_graphml(G, "fluid-communities.graphml")
    


    pdb.set_trace()
