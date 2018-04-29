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

    # if items is a single element list, just return the sole ReqList
    # no need to wrap another one around
    if len(items) == 1:
        return items[0]
    else:
        return ReqList(items, True)
    

# Takes a list of strings, which is the result of splitting a series on commas
# returns the parsed result in the form of a reqlists
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

# parses a raw prereq string from a catalog entry assuming the syntax laid out
# on the registrar's site
# returns a (nested) ReqList data structure
def parse_req_string(req_str):
    # split into semicolon-delimted series
    req_series = req_str.split(';')

    # split each series in classes
    req_classes = []

    for series in req_series:
        # trim whitespace from split result
        req_classes.append([i.strip() for i in series.split(',')])
    result = parse_requisite(req_classes)

    return result
        
