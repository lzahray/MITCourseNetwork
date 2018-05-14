import csv

from parse_req import parse_req_string
from prereqDataParser import Course

def ingest_catalog():

    courses = []
    subjectToMaster = {}
    subjectToMaster["PERMISSION"] = "PERMISSION"
    masterClassesSeen = set()
    with open('catalog.csv', 'rt') as csvfile: 
        reader = list(csv.reader(csvfile, delimiter=","))
        print("last row: ", reader[-1])
        print("second to last row: ", reader[-2])
        for row in reader[5:]:
            if not all(item == "" for item in row):
                subjectToMaster[row[1]] = row[2]
                if row[2] in masterClassesSeen:
                    #we've already done this class (effectively) - skip it
                    pass
                else:
                    newCourse = Course(row[2], parse_req_string(row[5]), None, row[4] == 'U')
                    courses.append(newCourse)
                    subjectToMaster[row[1]] = row[2]
                    masterClassesSeen.add(row[2])
                #if row[1]== "CC.8022":
                    #print("req string was ", row[5], " and it's set to ", courses[-1].preReqs)
        
    return courses, subjectToMaster

if __name__ == '__main__':
    courses, sub = ingest_catalog()
    for c in courses:
        print(c.__repr__())

