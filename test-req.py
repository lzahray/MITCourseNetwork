import pdb
from prereqDataParser import ReqList

# 031 AST? TODO
# Takes a list of lists of strings, each list representing a series that makes up the
# prerequiste
# Ands together the results of calling parse_clause on each of the series
def parse_requisite(req):
    # assert valid input
    for r in req:
        assert type(r) == list
        for s in r:
            assert type(s) == str

    items = [] 
    for r in req:
        items.append(parse_clause(r))
    return ReqList(items, True)
    

# Takes a list of strings, which is the result of splitting a series on commas
# returns the parsed result in the form of nested ReqLists
def parse_clause(clause):
    # assert correctness of input
    assert type(clause) == list
    for c in clause:
        assert type(c) == str

    # 1. check the last element for 'or'
    if 'or' in clause[-1]:
        items = []
        for element in clause[:-1]:
            items.append(element)
        #1a. Check if it is a 'or A and B' clause
        if 'and' in clause[-1]:
            # add the last 'or A and B' clause
            last_clause = clause[-1][3:]
            last_clause_ands = []
            for i in last_clause.split('and'):
                last_clause_ands.append(i)
            items.append(ReqList(last_clause_ands, True))
            return ReqList(items, False)
        # 1b. It is just a or A clause
        else:
            items.append(clause[:-1])
            return ReqList(items, False)
    # 2. The last element doesn't have or - all elements are anded
    else:
        items = []
        for element in clause:
            items.append(element)
        return ReqList(items, True) 

fi = open("sample-reqs.txt")


reqs = []

for line in fi:
    reqs.append(line[0:-2]) 
    
req_clauses = []
for req in reqs:
    req_clauses.append(req.split(';'))

req_classes = []

for clauses in req_clauses:
    tmp = []
    for clause in clauses:
        tmp.append(clause.split(','))
    req_classes.append(tmp)

result = parse_requisite(req_classes[0])

pdb.set_trace()

        
