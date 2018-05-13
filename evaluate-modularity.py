"""
 Calculate normalized mutual information of modularity.
"""

import csv
import sys
import sklearn.metrics
import networkx as nx
import pdb

def evaluate_nmi(filename, col_id, col_modularity):
    """
    Take a gephi graph output csv table and evaluate the mutual information
    on its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return normalized mutual information score
    """

    ids = []
    modularities = []

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            ids.append(row[col_id])
            modularities.append(row[col_modularity])

    return sklearn.metrics.normalized_mutual_info_score(ids, modularities)

def evaluate_purity(filename, col_id, col_modularity):
    """
    Take a gephi graph output csv table and calculate the purity
    score of its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return purity score
    """
    # TODO: this is just my own thing, might not actually be offical 'purity'
    ids = []
    modularities = []

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            ids.append(row[col_id])
            modularities.append(row[col_modularity])

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
            print(course, " is not ", maj_label[modularity])
            wrong +=1

    print("right: ",right)
    print("wrong: ",wrong)

    return right / (right + wrong)

def evaluate_f_measure(filename, col_id, col_modularity):
    """
    Take a gephi graph output csv table and evaluate the f-measure
    on its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return f-measure score
    """

    ids = []
    modularities = []

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            ids.append(row[col_id])
            modularities.append(row[col_modularity])

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

    
def evaluate_ari(filename, col_id, col_modularity):
    """
    Take a gephi graph output csv table and evaluate the adjusted rand index
    on its modularity and course number.

    :param str filename: Filename of csv file to load.
    :param int col_id: 0 indexed index of column containing course name
    :param int col_modularity: 0-indexed index of column containg modularity class
    :return adjusted rand index
    """

    ids = []
    modularities = []

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            ids.append(row[col_id])
            modularities.append(row[col_modularity])

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
def evaluate_directed_modularity(filename):
    """
    Take a .graphml file and evaluate the directed modularity of its classification.

    :param str filename: Filename of graphml file to load.
    :return modularity score of graph communities
    """

    G = nx.read_graphml(filename)
# function expects list of sets of nodes
    communities = {}

    for node in G.nodes(data=True):
        mod_class = node[1]['Modularity Class']
        print('mod_class: ',mod_class)
        if mod_class not in communities:
            communities[mod_class] = set([])
        print("node, ",node[0])
        communities[mod_class].add(node[0])

    return nx.algorithms.community.quality.modularity(G, list(communities.values()))



if __name__ == '__main__':
    try:
        assert len(sys.argv) == 4

        filename = sys.argv[1]
        col_id = int(sys.argv[2])
        col_modularity = int(sys.argv[3])

        # external evaluation metrics
        nmi_result = evaluate_nmi(filename, col_id, col_modularity)
        purity_result = evaluate_purity(filename, col_id, col_modularity)
        f1_result = evaluate_f_measure(filename, col_id, col_modularity)
        ari_result = evaluate_ari(filename, col_id, col_modularity)

        # internal evaluation metrics
        mod_result = evaluate_directed_modularity("gephi-files/community.graphml")

        print("--- External Evaluation Metrics ---")
        print("NMI: ",nmi_result)
        print("Purity: ",purity_result)
        print("F1 Measure: ",f1_result)
        print("Adjusted Rand Index: ", ari_result)


        print("--- Internal Evaluation Metrics ---")
        print("Directed Modularity: ", mod_result)
        




    except AssertionError:
        print("Usage: evaluate-modularity.py [filename] [col_id] [col_modularity]")
    



