import pdb

class Course():
    def __init__(self, name, preReqs,coReqs,undergrad):
        #coreqs is defunct
        self.name = name #course name
        #either one string (if one class is prereq) or one ReqList (ReqList is recursive)
        self.preReqs = preReqs 
        self.coReqs = coReqs
        self.undergrad = undergrad #true if Undergrad, false if grad
        self.course = name.split(".")[0] #for automatically getting course number
        self.runningInTotal = 0
        self.runningOutTotal = 0
        #self.possibilities = None #don't think we need this actually
    def __str__(self):
        return self.name

    def __repr__(self):
        return "Course("+self.name+","+str(self.preReqs)+","+(self.coReqs if self.coReqs != None else "None")+","+str(self.undergrad)+","+self.course+")"

    def set_runningInTotal(self,G):
        #G is the graph
        #do not call this function out of top sort order
        toPrint = False
        if self.name == "8.02":
            toPrint = True
        inTotal = 0
        for edge in list(G.in_edges(self)):
            weight = G.get_edge_data(*edge)["weight"]
            source = edge[0]
            inTotal += weight*(1+source.runningInTotal)
            if toPrint:
                print("source of ", source, "weight ", weight, " its running ", source.runningInTotal)
        if toPrint:
            print("about to set to ", inTotal)
        self.runningInTotal = inTotal           
            
    def set_runningOutTotal(self,G):
        #G is the graph
        #do not call this function out of top sort order
        #print("my name: ", self.name)
        outTotal = 0
        for edge in list(G.out_edges(self)):
            weight = G.get_edge_data(*edge)["weight"]
            dest = edge[1]
            #print("dest: ", dest.name)
            outTotal += weight*(1+dest.runningOutTotal)
        self.runningOutTotal = outTotal 


#example:
#x or (y and z) is ReqList([x, ReqList([y,z)],True)], False)

class ReqList():
    def __init__(self, items, isAnded):
        self.items = items #list of ReqLists and maybe strings
        self.isAnded = isAnded #true if logic of clause is AND, false if OR

    # equality defined as same isAnded and items value
    # item equality is checked recursively
    def __eq__(self, other):
        if other == None:
            return False

        if type(other) != ReqList:
            return False
    
        if self.isAnded != other.isAnded:
            return False
        # check that items are equal, recursively if there are nested ReqList's
        for i, item in enumerate(self.items):
            if other.items[i] != item:
                print("gonna be false because item is ", item, " and other is ", other.items[i])
                return False

        return True

    # return a human-readable string rep of the ReqList
    def __str__(self):
        return "{"+str(self.isAnded) + " " + str(self.items)+"}"

    def __repr__(self):
        return "ReqList("+repr(self.items)+", "+str(self.isAnded)+")"

    @staticmethod
    # takes a reqList and flattens nested ReqLists of the same isAnded value
    # also turns singleton reqlists (where only item is a string) into pure strings
    def flatten(reqList):

        # if not given a ReqList, just return it straightaway
        if type(reqList) != ReqList:
            return reqList

        isAnded = reqList.isAnded
        
        newItems = []


        for item in reqList.items:
            if type(item) is ReqList and item.isAnded == reqList.isAnded:
                newItems = newItems + item.items
            else:
                newItems.append(item)

        if len(newItems) == 1 and type(newItems[0]) == str:
            return newItems[0]



        return ReqList(newItems, isAnded)




        

        



##def representsCourse(s):
##    #Idea is to check if a word represents a course number (to find correct line in catalog)
##    #TODO: Incomplete, for now is checking if (without [J] it represents a float)
##    s = s.replace('[J]','')
##    try:
##        float(s)
##        return True
##    except ValueError:
##        return False
##
##def parsePrereqs(line):
##    #TODO
##    #this takes the prereq line of text and gets the prereqs into a form of ReqList(...)
##    #returns prereqs, coreqs 
##
##    print("Raw line: " + line)
##    
##    # strip off "Prereq: "
##    reqString = line[8:]
##
##    prereqFile.write(reqString+"\n")
##
##    # Case 1: permission of instructor
##    if reqString == "Permission of instructor":
##        print("returning None.")
##        # return nothing for now
##        return [None, None]
##
##    print("Strip raw into reqString:", reqString)


    
    # we will handle this by cases
##    return (ReqList(None, None), ReqList(None,None)) #REPLACE WITH REAL CODE 

##def createCourses(fileName, major):
##    #fileName is .txt with copy-paste from catalog
##    #NEED TO ADD [J] FUNCTIONALITY
##    with open(fileName) as f:
##        text = f.readlines()
##    text = [x.strip() for x in text]
##    i = 0 #i is the line we're on
##    while i < len(text):
##        line = text[i]
##        words = line.split()
##        if len(words) > 0:
##            if representsCourse(words[0]): #if we've reached a new course line
##                name = words[0] #get course name
##                i += 2 #skip the line with _____
##
##                #find out undergrad or grad
##                line = text[i]
##                words = line.split()
##                undergrad = True if words[0] == "Undergrad" else False
##                print(name,undergrad)
##                i += 1
##
##                #find prereq line
##                while text[i].split()[0] != "Prereq:":
##                    i += 1
##                line = text[i]
##                print(line) #prereq line 
##
##                #parse prereq line
##                preReqs, coReqs = parsePrereqs(line)
##
##                #add the course to the dictionary
##                courseDict[name] = Course(name, preReqs, coReqs, undergrad) #add course to dict
##        i += 1
##    return courseDict
