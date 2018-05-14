import csv

from parse_req import parse_req_string
from prereqDataParser import Course


girs = {"GIR:PHY2":["8.02","8.021","8.022","CC.802","CC.8022","ES.802","ES.8022"], "GIR:CAL1":["18.01","18.01A", "CC.181A","ES.1801","ES.181A"], "GIR:PHY1":["8.01","8.01L","8.011","8.012","CC.801","CC.8012","ES.801","ES.8012"],
                  "GIR:CHEM":["3.091","5.111","5.112","CC.5111","ES.3091","ES.5111","ES.5112"], "GIR:BIOL":["7.012","7.013","7.014","7.015","7.016","ES.7012","ES.7013"], "GIR:CAL2":["18.02","18.022","18.02A","CC.182A","CC.1802","ES.1802","ES.182A"]}
courseToGIR = {}
for key in girs:
    for course in girs[key]:
        courseToGIR[course] = key

def ingest_catalog():

    courses = []
    subjectToMaster = {}
    subjectToMaster["PERMISSION"] = "PERMISSION"
    for key in girs:
        subjectToMaster[key] = key
    masterClassesSeen = set()
    with open('catalog.csv', 'rt') as csvfile: 
        reader = list(csv.reader(csvfile, delimiter=","))
        print("last row: ", reader[-1])
        print("second to last row: ", reader[-2])
        for row in reader[5:]:
            if not all(item == "" for item in row):
                if row[1] in courseToGIR:
                    subjectToMaster[row[1]] = courseToGIR[row[1]]
                    #print("we're at ", row[1], "set to ", courseToGIR[row[1]])
                    #subjectToMaster[row[1]] = row[2]
                    pass
                else:
                    subjectToMaster[row[1]] = row[2]
                actualName = subjectToMaster[row[1]]
                if row[2] in masterClassesSeen:
                    #we've already done this class (effectively) - skip it
                    pass
                else:
                    newCourse = Course(actualName, parse_req_string(row[5]), None, row[4] == 'U', row[3])
                    courses.append(newCourse)
                    masterClassesSeen.add(actualName)
                #if row[1]== "CC.8022":
                    #print("req string was ", row[5], " and it's set to ", courses[-1].preReqs)
        
    return courses, subjectToMaster

if __name__ == '__main__':
    courses, sub = ingest_catalog()
    for c in courses:
        print(c.__repr__())

