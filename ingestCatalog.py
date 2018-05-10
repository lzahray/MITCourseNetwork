import csv

from parse_req import parse_req_string
from prereqDataParser import Course

def ingest_catalog():

    courses = []
    with open('catalog.csv', 'rt') as csvfile: 
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            courses.append(Course(row[2], parse_req_string(row[5]), None, row[4] == 'U'))

    return courses

if __name__ == '__main__':
    course = ingest_catalog()
    for c in courses:
        print(c.__repr__())

