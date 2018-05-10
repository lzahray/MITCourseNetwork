import pdb
from prereqDataParser import ReqList

# parses a raw prereq string from a catalog entry assuming the syntax laid out
# on the registrar's site
# returns a (nested) ReqList data structure
def parse_req_string(req_str):

    # note: prereq strings that contain 'with permission of instructor'
    # are special cases handled at a high level
    # our approach will be to detect these in the raw string, strip them out
    # and or them with the result of parsing the rest of the string

    # the main problem will be how to strip them out cleanly...
    # based off of looking at prereq strings, I'm asuming that 
    # the poi string always occurs at the end in the format
    # 'or permission of instructor'
    # 'or obtain permission of instructor'
    
    # first detect

    #NEW CODE HERE
    #split by semicolon first and formost
    req_str = req_str.upper()
    clauses = req_str.split(';')
    yesAndListSemi = [] #not including permission
    permissionAnd = False
    permissionOr = False
    #figure out logic of these clauses
    #this part might be problematic for weird cases where it's like A;and B; or C but like... eww what even is that
    for clause in clauses:
        clause = clause.strip(' ')
        words = clause.split(" ")
        if words[0] == "AND" or words[0] == "OR":
            yesAnd = words[0] == "AND"
            if clause.find("PERMISSION"):
                permissionAnd = yesAnd
                permissionOr = not yesAnd
            else:
                for i in range(len(yesAndListSemi)):
                    yesAndListSemi[i] = yesAnd
                    yesAndListSemi.append(yesAnd)
            #now we've taken care of it, no longer need the and/or at beginning
            clause = clause.strip("AND ").stip("OR ")
        else:
            #default is and if not specified, may be overwritten later 
            yesAndListSemi.append(True)
    #first off let's delete the permission clause
    if permissionAnd or permissionOr:
        clauses.pop()
    #now we can separate by comma
    #yes we do need a new loop sorry y'all
    finalItems = []
    for i in range(len(clauses)):
        clause = clauses[i]
        #clause is something that was separated by semicolons
        clause = clause.strip(' ')
        subclauses = clause.split(", ")
        #almost to the base case except, not quite!! could have A or B
        #we do need to figure out whether everything is anded or ored, do procedure from above
      
        items = []
        yesAndComma = True
        for j in range(len(subclauses)):
            subclause = subclauses[j].strip(' ')
            words = subclause.split(' ')
            if j == len(subclauses)-1: #if it's the last clause there might be some AND/OR logics going on
                if subclause.find("AND") >=0:
                       yesAndComma = True
                       if words[0] == "AND":
                           words.pop(0)
                           subclause = subclause[3:]
                elif subclause.find("OR") >=0:
                       yesAndComma = False
                       if words[0] == "OR":
                           words.pop(0)
                           subclause = subclause[3:]                                              
                    
            if len(words) == 1: #one class
                items.append(words[0])
            elif len(words) == 3:
                #we're just assuming A or B format otherwise sadness
                if subclause.find("AND") >=0:
                    items.append(ReqList([words[0], words[2]],True)) 
                elif subclause.find("OR")>=0:
                    items.append(ReqList([words[0], words[2]],False))
                else:
                    print("AHHHH WHAT WE'RE SKIPPING THIS ONE FOLKS")
                    return None
            else:
                print("AHHHH WHAT WE'RE SKIPPING THIS ONE FOLKS")
                return None
        if len(items) == 1:
            finalItems.append(items[0])
        elif len(items) == 0:
            return None
        else:
            finalItems.append(ReqList(items,yesAndComma))

    if len(finalItems) == 1:
        return finalItems[0]
    elif len(finalItems) == 0:
        return None
    else:
        if permissionOr:
            return ReqList([ReqList(finalItems,yesAndListSemi[0]),"permission"],False)
        elif permissionAnd:
            return ReqList([ReqList(finalItems,yesAndListSemi[0]),"permission"],True)
        else:
            return ReqList(finalItems,yesAndListSemi[0])
        
                
                
                
    





##    ####OLD CODE HERE
##    poi_present = False
##    
##    # handle two cases separetly
##    if "or permission of instructor" in req_str or "or obtain permission of instructor" in req_str:
##        # then cleanly strip out
##        # sanity check that the last or is close enough to the last permission
##        print("req_str: ", req_str)
##        print("last or: ", req_str.rfind(" or "))
##        print("last permission: ", req_str.rfind("permission"))
##        assert abs(req_str.rfind(" or ") - req_str.rfind("permission")) <= len("or obtain ")
##
##
##        req_str = req_str[:req_str.rfind(" or ")]
##        print("after strip: ",req_str)
##
##        poi_present = True
##    elif "permission of instructor" in req_str:
##        print("poi handled at high level")
##        req_str = req_str[:req_str.rfind("permission")]
##        poi_present = True
##
##
##
##
##
##    # split into semicolon-delimted series
##    req_series = req_str.split(';')
##
##    # split each series in classes
##    req_classes = []
##
##    for series in req_series:
##        # skip if empty
##        if len(series) == 0:
##            continue
##        # trim whitespace from split result
##        req_classes.append([i.strip() for i in series.split(',')])
##    result = parse_requisite(req_classes)
##
##    if poi_present:
##        result = ReqList([result, "permission"], False)
##
##    return result

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
        # check special case singleton "permission of instructor"
        #if "permission of instructor" in items[0]:
        #    return "permission"
        #else:
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
    if 'or' in clause[-1].strip():
        items = []
        for element in clause[:-1]:
            items.append(element)
        #1a. Check if it is a 'or A and B' clause
        if 'and' in clause[-1]:
            # add the last 'or A and B' clause
            last_clause = clause[-1][3:]
            last_clause_ands = []
            for i in last_clause.split('and'):
                last_clause_ands.append(i.strip())
            assert len(last_clause_ands) > 1
            items.append(ReqList(last_clause_ands, True))
            return ReqList(items, False)
        # 1b. It is just a or A clause
        else:
            last_class = clause[-1].split(" ")[1]
            # if it is a "..., or permission of instructor"
            if "permission of instructor" in last_class:
                items.append("permission")
            else:
                # format is 'or class' - we want class
                items.append(last_class)

            # return singleton object if only one item
            if len(items) == 1:
                return items[0]
            else:
                return ReqList(items, False)
    # 2. The last element doesn't have or - all elements are anded
    else:
        items = []
        for element in clause:
            items.append(element)

        # convention is not to return singleton ReqLists
        if len(items) == 1:
            return items[0]
        else:
            return ReqList(items, True) 

        
