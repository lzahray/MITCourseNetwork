import networkx as nx
import pdb
import itertools
import numpy as np

import community
import sys
import math



if __name__ == '__main__':
    G = nx.read_graphml(sys.argv[1])
    filename = sys.argv[1].split('.')[0]
    num_comm = int(sys.argv[2])


    G_u = G.to_undirected()

    G_u.remove_nodes_from(list(nx.isolates(G_u)))
    
    sc = sorted(list(nx.connected_component_subgraphs(G_u)), reverse=True, key = lambda x: len(x.nodes()))

    for c in sc:
        l = len(c.nodes())
        if l < 5:
            print("cutting off")
            break
        else:
            print(len(c.nodes()))
    
    out_dict = {}

    target_size = len(G_u.nodes()) / num_comm

    # get connected components
    for cc in sc:
        # when doing multiple components, offset so we have unique numbers across components
        if len(out_dict) > 0:
            print("computing offset, dict values=", set(out_dict.values()))
            comm_offset = max(out_dict.values()) + 1
        else:
            comm_offset = 0

        print(len(cc.nodes()))
        comp_size = len(cc.nodes())
        
        print("comm offset: ",comm_offset)


        comm_in_components = max(round(comp_size / target_size), 1)
        print(comp_size)
        print(target_size)
        print(comm_in_components)
        result = nx.algorithms.community.asyn_fluidc(cc, comm_in_components)

        for i, r in enumerate(result):
            for c in r:
                G.add_node(c, fluid_comm = i+comm_offset)
                out_dict[c] = i+comm_offset

        np.save("comm-data/fluid.npy", np.asarray(out_dict))

    print(len(out_dict), " out of ", len(G_u.nodes()))
    pdb.set_trace()

    nx.write_graphml(G, "{1}_fluid-communities-{0}_comms.graphml".format(num_comm, filename))
    print("saved to ", "{1}_fluid-communities-{0}_comms.graphml".format(num_comm, filename))
 

