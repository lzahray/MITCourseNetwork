"""
 Calculate normalized mutual information of modularity.
"""

import csv
import sys
import sklearn.metrics
import networkx as nx
import pdb
import glob
import numpy as np

def evaluate_nmi(courses, modularities):
    """
    Take a gephi graph output csv table and evaluate the mutual information
    on its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return normalized mutual information score
    """

    return sklearn.metrics.normalized_mutual_info_score(courses, modularities)

def evaluate_purity(ids, modularities):
    """
    Take a gephi graph output csv table and calculate the purity
    score of its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return purity score
    """

    

    # find the percent of courses that agree with the majority in their
    # modularity group
    # figure out a 'guessed' course by taking the majority course in each modularity class
    
    modularity_courses = {} # dict mapping m class to dict that maps courses ot counts
    for course, modularity in zip(ids, modularities):
        course_num = course.split('.')[0]

        # initialize if empty
        if modularity not in modularity_courses:
            modularity_courses[modularity] = {}
        if course_num not in modularity_courses[modularity]:
            modularity_courses[modularity][course_num] = 0

        modularity_courses[modularity][course_num] += 1

    # map modularity id to course
    maj_label = {}
    for m in modularity_courses:
        maj_label[m] = max(modularity_courses[m].keys(), key = lambda x: modularity_courses[m][x])


    right = 0
    wrong = 0

    for course, modularity in zip(ids, modularities):
        course_num = course.split('.')[0]
        if maj_label[modularity] == course_num:
            right += 1
        else:
            wrong +=1

    return right / (right + wrong)

def evaluate_f_measure(ids, modularities):
    """
    Take a gephi graph output csv table and evaluate the f-measure
    on its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return f-measure score
    """

    # find the percent of courses that agree with the majority in their
    # modularity group
    # figure out a 'guessed' course by taking the majority course in each modularity class
    
    modularity_courses = {} # dict mapping m class to dict that maps courses ot counts
    for course, modularity in zip(ids, modularities):
        course_num = course.split('.')[0]

        # initialize if empty
        if modularity not in modularity_courses:
            modularity_courses[modularity] = {}
        if course_num not in modularity_courses[modularity]:
            modularity_courses[modularity][course_num] = 0

        modularity_courses[modularity][course_num] += 1

    # map modularity id to course
    maj_label = {}
    for m in modularity_courses:
        maj_label[m] = max(modularity_courses[m].keys(), key = lambda x: modularity_courses[m][x])
    
    
    return sklearn.metrics.f1_score([maj_label[m] for m in modularities], [i.split('.')[0] for i in ids], average='weighted')

    
def evaluate_ari(ids, modularity):
    """
    Take a gephi graph output csv table and evaluate the adjusted rand index
    on its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return adjusted rand index
    """


    # find the percent of courses that agree with the majority in their
    # modularity group
    # figure out a 'guessed' course by taking the majority course in each modularity class
    
    modularity_courses = {} # dict mapping m class to dict that maps courses ot counts
    for course, modularity in zip(ids, modularities):
        course_num = course.split('.')[0]

        # initialize if empty
        if modularity not in modularity_courses:
            modularity_courses[modularity] = {}
        if course_num not in modularity_courses[modularity]:
            modularity_courses[modularity][course_num] = 0

        modularity_courses[modularity][course_num] += 1

    # map modularity id to course
    maj_label = {}
    for m in modularity_courses:
        maj_label[m] = max(modularity_courses[m].keys(), key = lambda x: modularity_courses[m][x])
    
    
    return sklearn.metrics.adjusted_rand_score([maj_label[m] for m in modularities], [i.split('.')[0] for i in ids])
def evaluate_directed_modularity(filename, attr):
    """
    Take a .graphml file and evaluate the directed modularity of its classification.

    :param str filename: Filename of graphml file to load.
    :param atr attr: node attribute name used for community label
    :return modularity score of graph communities
    """
    default_label = 1000

    G = nx.read_graphml(filename)
    communities = {}
    # function expects list of sets of nodes
    for node in G.nodes(data=True):
        if attr not in node[1]:
            mod_class = default_label # put all non classified nodes into some default community
        else:
            mod_class = node[1][attr]
        if mod_class not in communities:
            communities[mod_class] = set([])
        communities[mod_class].add(node[0])
    print(filename, " ",attr)
    print(len(communities.keys()), " communities.")


    print(nx.algorithms.community.quality.modularity(G, list(communities.values())))



if __name__ == '__main__':
    filename = "fluid-communities.graphml"

    evaluate_directed_modularity("fluid-communities.graphml", 'fluid_comm')
    evaluate_directed_modularity("indegreeGIRsGrouped.graphml", "course")
    evaluate_directed_modularity("outdegreeGIRsGrouped.graphml", "course")



    
    try:
        # evaluate all the npy files in a directory
        directory = "comm-data/"

        nmi = []
        purity = []
        f1 = []
        ari = []
        mod = []

        points = []

        for f in glob.glob(directory+"*.npy"):
            print("===")
            print("===")
            print("===")
            print(f)

            points.append(float(f.split("-")[2][:-4]))

            x = np.load(f)
            x = x[()]

            ids = list(x.keys())
            modularities = ([x[i] for i in ids])


            print("--- External Evaluation Metrics ---")
            # external evaluation metrics
            nmi_result = evaluate_nmi(ids, modularities)
            print("NMI: ",nmi_result)
            purity_result = evaluate_purity(ids, modularities)
            print("Purity: ",purity_result)
            f1_result = evaluate_f_measure(ids, modularities)
            print("F1 Measure: ",f1_result)
            ari_result = evaluate_ari(ids, modularities)
            print("Adjusted Rand Index: ", ari_result)

            print("--- Internal Evaluation Metrics ---")
            # internal evaluation metrics
            mod_result = evaluate_directed_modularity("gephi-files/community.graphml")
            print("Directed Modularity: ", mod_result)

            nmi.append(nmi_result)
            purity.append(purity_result)
            f1.append(f1_result)
            ari.append(ari_result)
            mod.append(mod_result)

        pdb.set_trace()

    


        




    except AssertionError:
        print("Usage: evaluate-modularity.py [filename]")
    



