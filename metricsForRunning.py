import networkx as nx
import createGraph

G = createGraph.actuallyMakeGraph(False)
inDegrees = nx.get_node_attributes(G, "runningInTotal")
numNodesPerDep = {}
numNodesPerDepNonzero = {}
depAvg = {}
depAvgNonzero = {}
for node in inDegrees:
    numNodesPerDep[node.course] = numNodesPerDep.get(node.course,0) + 1
    if node.runningInTotal >0:
        numNodesPerDepNonzero[node.course] = numNodesPerDepNonzero.get(node.course,0) + 1
        depAvgNonzero[node.course] = depAvgNonzero.get(node.course,0) + node.runningInTotal
    depAvg[node.course] = depAvg.get(node.course,0) + node.runningInTotal
    

for dep in depAvg:
    depAvg[dep] = depAvg[dep]/numNodesPerDep[dep]
    if depAvg[dep] != 0:
        depAvgNonzero[dep] = depAvgNonzero[dep]/numNodesPerDepNonzero[dep]

#print (depAvg)
sortedValues = []
sortedValuesNonzero=[]
for dep in depAvg:
    sortedValues.append((dep,depAvg[dep]))
    if depAvg[dep] != 0:
        sortedValuesNonzero.append((dep,depAvgNonzero[dep]))
sortedValues = sorted(sortedValues, key=lambda x:x[1])
sortedValuesNonzero = sorted(sortedValuesNonzero, key=lambda x:x[1])

for thing in sortedValues:
    print("including zeros: ",thing)
for thing in sortedValuesNonzero:
    print("NOT including zeros: ", thing)
