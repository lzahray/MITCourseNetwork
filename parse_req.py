import pdb
from prereqDataParser import ReqList

# parses a raw prereq string from a catalog entry assuming the syntax laid out
# on the registrar's site
# returns a (nested) ReqList data structure
specialStrings = {"GIR:PHY2":ReqList(["8.02","8.021","8.022","CC.802","CC.8022","ES.802","ES.8022"],False), "GIR:CAL1":ReqList(["18.01","18.01A","18.014", "CC.181A","ES.1801","ES.181A"],False), "GIR:PHY1":ReqList(["8.01","8.01L","8.011","8.012","CC.801","CC.8012","ES.801","ES.8012"],False),
                  "GIR:CHEM":ReqList(["3.091","5.111","5.112","CC.5111","ES.3091","ES.5111","ES.5112"],False), "GIR:BIOL":ReqList(["7.012","7.013","7.014","7.015","7.016","ES.7012","ES.7013"],False), "GIR:CAL2":ReqList(["18.02","18.022","18.02A","CC.182A","CC.1802","ES.1802","ES.182A"],False)}
stringsToChangeLong = {"PHYSICS II":"GIR:PHY2","PERMISSION OF IDSS ACADEMIC OFFICE.":"PERMISSION", "PERMISSION OF TPP ACADEMIC OFFICE.":"PERMISSION","FIRST-YEAR UNDERGRADUATE STANDING":'',"COMMITMENT TO REGISTER AS A FRESHMAN IN THE FALL":'',
                  "ONE INTERMEDIATE SUBJECT IN FRENCH":'',"MUST APPLY TO THE GRADUATE CONSORTIUM IN WOMEN'S STUDIES":'', "ONE CI-H/HW SUBJECT":'',"ONE CI-H/CI-HW SUBJECT":'','Must have read "The Society of Mind" and "The Emotion Machine"'.upper(): '',
                   "RECOMMENDED BUT NOT NECESSARY":'',"Knowledge of differentiation and elementary integration".upper():'',"ONE SUBJECT IN COMPARITIVE MEDIA STUDIES":'',"ONE SUBJECT IN CMS OR MAS":'',
                   "WRITING SAMPLE":'',"A FICTION WORKSHOP":'',"PRIOR MANUSCRIPT SUBMISSION REQUIRED":'',"[PARTICIPATION IN ENSEMBLE FOR VOCALISTS]":'',"ONE SUBJECT IN FILM, MUSIC, OR THEATER":'',"ONE INTERMEDIATE SUBJECT IN SPANISH":'',"ONE INTERMEDIATE SPANISH SUBJECT":'',"PERMISSION OF ADVISOR":'PERMISSION',
                   "PLACEMENT EXAM AND":'',"ONE SUBJECT IN LITERATURE OR COMPARATIVE MEDIA STUDIES":'',"PERMISSION OF THE DIRECTOR OF COMPARATIVE MEDIA STUDIES":'',"TWO SUBJECTS IN LITERATURE OR COMPARATIVE MEDIA STUDIES":'',"TWO SUBJECTS IN LITERATURE OR HISTORY":'',"PLACEMENT TEST AND ":'',"FLUENCY IN A SPANISH DIALECT":'', "PERMISSION OF DIRECTOR OF COMPARATIVE MEDIA STUDIES":'',
                       "BASED ON PREVIOUS COURSEWORK":'',"One philosophy subject or one subject on probability".upper():'',"PERMISSION OF RESEARCH SUPERVISOR":'PERMISSION',"PERMISSION OF INSTRUCTORS":"PERMISSION", "AS SPECIFIED FOR PARTICULAR FIELD":'',"Two mathematics subjects numbered 18.100 or above".upper():'', "ANY TWO SUBJECTS IN PHILOSOPHY":'',
                       "SOME FAMILIARITY WITH LIE THEORY":'',"FRESHMEN NEED PERMISSION OF INSTRUCTOR":'',"PERMISSION OF DEPARTMENT":'PERMISSION',"Graduate-level fluid mechanics and a subject on waves".upper():'',"OTHER INTRODUCTORY ASTRONOMY COURSE":'',"OPEN TO UNDERGRADUATES WITH PERMISSION OF INSTRUCTOR":'',"BY PERMISSION O INSTRUCTOR":"PERMISSION",
                       "introductory subject in thermodynamics or physical chemistry".upper():'',"any other two subjects in Brain and Cognitive Sciences".upper():'',"AN APPROVED RESEARCH EXPERIENCE":'',"High school course covering cellular and molecular biology".upper():'',"SEE MODULE DESCRIPTIONS UNDER SUBJECT 5.35":'',"SEE MODULE DESCRIPTIONS UNDER SUBJECT 5.36":'',"SEE MODULE DESCRIPTIONS UNDER SUBJECT 5.37":''}
stringsToChangeShort = {"ONE SUBJECT IN LITERATURE":'',"TWO SUBJECTS IN FILM AND MEDIA":'',"TWO SUBJECTS IN LITERATURE":'', "TWO HISTORY SUBJECTS":'',"TWO SUBJECTS IN ANTHROPOLOGY":'',"RECOMMENDED FIRST CLASS CRUISE AND":'',"ONE D-LAB SUBJECT":'',"ONE PHILOSOPHY SUBJECT":'',"PERMISSION OF INSTRUCTOR":"PERMISSION","SEE MODULE DESCRIPTIONS":'',
                        "ONE SUBJECT IN COMPARATIVE MEDIA STUDIES":'',"TWO CMS SUBJECTS":'',"TWO SUBJECTS IN PHILOSOPHY":'',"PERMISSION OF THE INSTRUCTOR":"PERMISSION", "PERMISSION OF INSTRCTOR":'', "ONE PHILOSOPHY SUBJECT":''}

#delete weird words
def parse_req_string(req_str):
    #NEW CODE HERE
    #split by semicolon first and formost

    #permission base case
    req_str = req_str.upper()
    for key in stringsToChangeLong:
        req_str = req_str.replace(key,stringsToChangeLong[key])
    for key in stringsToChangeShort:
        req_str = req_str.replace(key,stringsToChangeShort[key])
    req_str = req_str.replace('[','').replace(']','')
    clauses = req_str.split(';')
    yesAndListSemi = [] #not including permission
    permissionAnd = False
    permissionOr = False
    

    
    #figure out logic of these clauses
    #this part might be problematic for weird cases where it's like A;and B; or C but like... eww what even is that
    for i in range(len(clauses)):
        
        clauses[i] = clauses[i].strip(" ")
        clause = clauses[i]
        #print("we're going through at least one clause and it's ", clause)
        #print("looking at clause: ", clause)
        words = clause.split(" ")
        if words:
            if words[0] == "AND" or words[0] == "OR":
                yesAnd = words[0] == "AND"
                if clause.find("PERMISSION") >= 0:
                    #print("we found permission in loop")
                    permissionAnd = yesAnd
                    permissionOr = not yesAnd
                else:
                    for j in range(len(yesAndListSemi)):
                        yesAndListSemi[j] = yesAnd
                        yesAndListSemi.append(yesAnd)
                #now we've taken care of it, no longer need the and/or at beginning
                clauses[i] = clause.strip("AND ").strip("OR ")
                #print("clauses currently in loop: ", clauses)
            else:
                #default is and if not specified, may be overwritten later 
                yesAndListSemi.append(True)
    #first off let's delete the permission clause
    if permissionAnd or permissionOr:
        #print("permission is a thing")
        clauses.pop()

    #now we can separate by comma
    #yes we do need a new loop sorry y'all
    finalItems = []
    for i in range(len(clauses)):
        
        
        clause = clauses[i]
        #print("clause is ", clause, " index ", i)
        #clause is something that was separated by semicolons
        clause = clause.strip(' ')
        subclauses = clause.split(", ")
        #almost to the base case except, not quite!! could have A or B
        #we do need to figure out whether everything is anded or ored, do procedure from above
      
        items = []
        yesAndComma = True
        for j in range(len(subclauses)):
            subclause = subclauses[j].strip(' ')
            #print("subclause: ",subclause)
            #print("subclause is ", subclause)
            words = subclause.split(' ')
            if words:
                if j == len(subclauses)-1: #if it's the last clause there might be some AND/OR logics going on
                    if words[0] == "AND":
                       yesAndComma = True
                       words.pop(0)
                       subclause = subclause[4:]
                    elif words[0] == "OR":                       
                       yesAndComma = False
                       words.pop(0)
                       #print("found an or and words are ", words)
                       subclause = subclause[3:]
                    elif subclause.find("AND") >= 0:
                        yesAndComma = True
                    elif subclause.find("OR") >= 0:
                        yesAndComma = False
                elif words[0] == "AND":
                    yesAndComma = True
                    words.pop(0)
                    subclause = subclause[4:]
                elif words[0] == "OR":
                    yesAndComma = False
                    words.pop(0)
                    subclause = subclause[3:]
                #print("subclause is ", subclause)
                #print("words are ", words)
                result = itemFromWords(words,subclause)
                if result:
                    items.append(result)                      

        if len(items) == 1:
            finalItems.append(items[0])
        elif len(items)!=0:
            finalItems.append(ReqList(items,yesAndComma))

    if len(finalItems) == 1:
        if permissionOr:
            return ReqList([finalItems[0],"PERMISSION"],False)
        elif permissionAnd:
            return ReqList([finalItems[0],"PERMISSION"],True)
        else:
            return finalItems[0]
    elif len(finalItems) == 0:
        if permissionOr or permissionAnd:
            return "PERMISSION"
        else:
            return None
    else:
        if permissionOr:
            return ReqList([ReqList(finalItems,yesAndListSemi[0]),"PERMISSION"],False)
        elif permissionAnd:
            return ReqList([ReqList(finalItems,yesAndListSemi[0]),"PERMISSION"],True)
        else:
            return ReqList(finalItems,yesAndListSemi[0])
        
def special(word):
    if word in specialStrings:
        return specialStrings[word]
    else:
        return word
                
def itemFromWords(words,subclause):
    if len(words) == 1: #one class
        if words[0] != "OR" and words[0] != "AND":
            return special(words[0])
    elif len(words) == 2:
        if words[0] == "AND" or words[0] == "OR": #something funky got deleted that no longer exists
            return special(words[1])
        elif words[1] == "AND" or words[1] == "AND":
            return special(words[0])
    elif len(words) == 3:
        #we're just assuming A or B format otherwise sadness
        if subclause.find("AND") >=0:
            return ReqList([special(words[0]), special(words[2])],True)
        elif subclause.find("OR")>=0:
            return ReqList([special(words[0]), special(words[2])],False)
        else:
            print("well that's weird the words are ", words)
            return None
    else:
        print("wasn't 1 2 or 3 the words are ", words)
        return None
