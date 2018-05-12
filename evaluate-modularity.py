"""
 Calculate normalized mutual information of modularity.
"""

import csv
import sys
import sklearn.metrics
import pdb

def evaluate(filename, col_id, col_modularity):
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

    #return sklearn.metrics.normalized_mutual_info_score(ids, modularities)


    # Alternatively, find the percent of courses that agree with the majority in their
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



if __name__ == '__main__':
    try:
        assert len(sys.argv) == 4

        filename = sys.argv[1]
        col_id = int(sys.argv[2])
        col_modularity = int(sys.argv[3])

        result = evaluate(filename, col_id, col_modularity)

        print(result)
    except AssertionError:
        print("Usage: evaluate-modularity.py [filename] [col_id] [col_modularity]")
    



