class Course():
    def __init__(self, name, preReqs,coReqs,undergrad):
        self.name = name #course name
        #either one string (if one class is prereq) or one ReqList (ReqList is recursive)
        self.preReqs = preReqs 
        self.coReqs = coReqs
        self.undergrad = undergrad #true if Undergrad, false if grad
        self.course = name.split(".")[0] #for automatically getting course number

#example:
#x or (y and z) is ReqList([x, ReqList([y,z)],True)], False)

class ReqList():
    def __init__(self, items, isAnded):
        self.items = items #list of ReqLists and maybe strings
        self.isAnded = isAnded #true if logic of clause is AND, false if OR

#GIRs that are listed weirdly in Course Catalog
calculusI = ReqList(["18.01","18.01A","18.014"],False)
calculusII = ReqList(["18.02","18.02A","18.022","18.023","18.024"],False)
physicsI = ReqList(["8.01","8.01L","8.011","8.012"],False)
physicsII = ReqList(["8.02","8.022"],False) #INCOMPLETE
permission = "permission"

def representsCourse(s):
    #Idea is to check if a word represents a course number (to find correct line in catalog)
    #TODO: Incomplete, for now is checking if (without [J] it represents a float)
    s = s.replace('[J]','')
    try:
        float(s)
        return True
    except ValueError:
        return False

def parsePrereqs(line):
    #TODO
    #this takes the prereq line of text and gets the prereqs into a form of ReqList(...)
    #returns prereqs, coreqs 
    return (ReqList(None, None), ReqList(None,None)) #REPLACE WITH REAL CODE 

courseDict = {}
def createCourses(fileName, major):
    #fileName is .txt with copy-paste from catalog
    #NEED TO ADD [J] FUNCTIONALITY
    with open(fileName) as f:
        text = f.readlines()
    text = [x.strip() for x in text]
    i = 0 #i is the line we're on
    while i < len(text):
        line = text[i]
        words = line.split()
        if len(words) > 0:
            if representsCourse(words[0]): #if we've reached a new course line
                name = words[0] #get course name
                i += 2 #skip the line with _____

                #find out undergrad or grad
                line = text[i]
                words = line.split()
                undergrad = True if words[0] == "Undergrad" else False
                print(name,undergrad)
                i += 1

                #find prereq line
                while text[i].split()[0] != "Prereq:":
                    i += 1
                line = text[i]
                print(line) #prereq line 

                #parse prereq line
                preReqs, coReqs = parsePrereqs(words)

                #add the course to the dictionary
                courseDict[name] = Course(name, preReqs, coReqs, undergrad) #add course to dict
        i += 1
    return courseDict
