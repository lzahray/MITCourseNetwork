from prereqDataParser import *
from itertools import product
import networkx as nx
import matplotlib.pyplot as plt
# import pdb 

# pdb.__trace__
def getAllPossibilities(parentReqs):
    #base case if parentReqs is a string
    #we never want to return anything other than a list of lists of strings. NO DEEPER
    if parentReqs == None:
        return []
    if type(parentReqs) == str:
        return [parentReqs] #maybe this should be a list?
    else:
        numItems = len(parentReqs.items)
        if parentReqs.isAnded:
            #print("And")
            #problem: we need to reduce one level of listiness  
            possibilities = []
            for i in range(numItems):
                #the thing we're appending is a list of lists of strings. 
                possibilities.append(getAllPossibilities(parentReqs.items[i]))
            #possibilities is a list of (list of lists of strings)
            almostFinal = list(product(*possibilities))
            #print("almostFinal: ", almostFinal)
            #it's *almost* final, we just have one too many layers of parens inside. Really just need to delete them.
            final = []
            for i in range(len(almostFinal)):
                #print("len(almostFinal): ", len(almostFinal))
                final.append([])
                for j in range(len(almostFinal[i])):
##                    print("len(almostFinal[i] ", len(almostFinal[i]))
##                    print("i is ", i)
##                    print("j is ", j)
##                    print("almostFinal is ", almostFinal)
##                    print("almostFinal[i] is", almostFinal[i])
                    #this is the deepness we want to be at
##                    print("almostFinal[i][j] is ", almostFinal[i][j])
                    if type(almostFinal[i][j]) != str:
                        for k in range(len(almostFinal[i][j])):
                            final[i].append(almostFinal[i][j][k])
                    else:
                        final[i].append(almostFinal[i][j])
            #print("Final: ", final)
            return final
        else:
            #for now same line as other case, if it stays can take it out of if/else
            possibilities = []
            for i in range(numItems):
                possibilities.append(getAllPossibilities(parentReqs.items[i]))
            #final really is just one of the things that ends up in possibilities
            #possibilities is a list of (list of lists of strings)
            #we really just want one of the lists of strings as each element in final
            final = []
            for i in range(len(possibilities)):
                for j in range(len(possibilities[i])):
                    final.append(possibilities[i][j])
            return final

def create_course_dict(courseList):
    course_dict = {}
    
    for course in courseList:
        if course.name not in course_dict:
            course_dict[course.name] = course
        else:
            print("found duplicate course for: ", course.name)

    return course_dict


def createGraph(courseDict, outdegree):
    #outdegree is True for outdegree graph, False for indegree graph
    G = nx.DiGraph()
    #nodes
    for courseName in courseDict.keys():
        course = courseDict[courseName]
        G.add_node(course.name, course = course.course, undergrad=course.undergrad)
    #edges
    for courseName in courseDict.keys():
        #print("courseName: ",courseName)
        course = courseDict[courseName]
        possibilities = getAllPossibilities(course.preReqs)
        print(courseName, ": ", possibilities)
        if outdegree:
            currentScore = getOutdegreeDict(possibilities)
        else:
            currentScore = getIndegreeDict(possibilities)
        for preReq in currentScore.keys():
            if preReq not in courseDict:
                courseOfPreReq = Course(preReq, None, None, True)
            else:
                courseOfPreReq = courseDict[preReq]
            
            G.add_edge(courseOfPreReq,course,weight=currentScore[preReq])
    return G

def getOutdegreeDict(possibilities):
    currentScore = {}
    for poss in possibilities:
        for c in poss:
            currentScore[c] = currentScore.get(c,0) + 1.0/(len(poss)*len(possibilities))
    return currentScore

def getIndegreeDict(possibilities):
    currentScore = {}
    for poss in possibilities:
        for c in poss:
            currentScore[c] = currentScore.get(c,0) + 1.0/(len(possibilities))
    return currentScore

#A B C D E F G H I J
courseTest = {"A": Course("A",ReqList(["D","C"],True), None,True), 
    "B": Course("B",ReqList([ReqList(["E",ReqList(["A","D"],True),"C"],False),"G"],True), None,True),
    "C": Course("C", None, None,True),
    "D": Course("D",ReqList(["H"],True), None,True),
    "E": Course("E",ReqList(["G","F",ReqList(["H","I"],False)],True), None,True),
    "F": Course("F",ReqList(["J","I","G"],False), None,True),
    "G": Course("G", None, None,True),
    "H": Course("H", "I", None,True),
    "I": Course("I", None, None,True),
    "J": Course("J", None, None,True)
    
    }

# catalog test
from ingestCatalog import ingest_catalog
import pdb
courseList = ingest_catalog()
courseDict = create_course_dict(courseList)
G = createGraph(courseDict, True)

pdb.set_trace()
#figure out edge weights
#figure out directed 
#G = createGraph(courseTest,True)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
labels = {}
for idx, node in enumerate(G.nodes()):
    labels[node] = node.name
edge_labels = {}
for idx, edge in enumerate(G.edges(data=True)):
    #print("edge: ",edge)
    edge_labels[(edge[0],edge[1])] = '{:0.3f}'.format(edge[2]['weight'])
nx.draw_networkx_labels(G,pos,labels)
nx.draw_networkx_edge_labels(G,pos,edge_labels,font_size=6)

# save to graphml file
nx.write_graphml(G, "thisbetterwork.graphml")

plt.show()
    # #base case is when the list is all strings:
    # numItems = len(parentReqs.items)
    # numString = 0
    # for i in range(numItems):
    #   if type(parentReqs.items[i]) == str:
    #       numString += 1
    # if numString == numItems:
    #   #BASE CASE
    #   if parentReqs.isAnded:
    #       return parentReqs.items[:] 
    #   else:
    #       possibilities = []
    #       for i in range(numItems):
    #           possibilities.append([parentReqs.items[i]])
    #       return possibilities
    # else:
    #   #let's think about the case where we have 2 strings and 1 reqList




        


#if i were doing it by hand, I'd look at the smallest guy first, at some point somebody has
#to be just made up of strings. Then if it's and, we return a list of all those. 
#if it's or, we return several lists of the individuals. 
