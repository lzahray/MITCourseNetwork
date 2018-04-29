from prereqDataParser import *
from itertools import product
# import pdb 

# pdb.__trace__
def getAllPossibilities(parentReqs):
    #base case if parentReqs is a string
    #we never want to return anything other than a list of lists of strings. NO DEEPER
    if type(parentReqs) == str:
        return [parentReqs] #maybe this should be a list?
    else:
        numItems = len(parentReqs.items)
        if parentReqs.isAnded:
            print("And")
            #problem: we need to reduce one level of listiness  
            possibilities = []
            for i in range(numItems):
                #the thing we're appending is a list of lists of strings. 
                possibilities.append(getAllPossibilities(parentReqs.items[i]))
            #possibilities is a list of (list of lists of strings)
            almostFinal = list(product(*possibilities))
            print("almostFinal: ", almostFinal)
            #it's *almost* final, we just have one too many layers of parens inside. Really just need to delete them.
            final = []
            for i in range(len(almostFinal)):
                print("len(almostFinal): ", len(almostFinal))
                final.append([])
                for j in range(len(almostFinal[i])):
##                    print("len(almostFinal[i] ", len(almostFinal[i]))
##                    print("i is ", i)
##                    print("j is ", j)
##                    print("almostFinal is ", almostFinal)
##                    print("almostFinal[i] is", almostFinal[i])
                    #this is the deepness we want to be at
##                    print("almostFinal[i][j] is ", almostFinal[i][j])
                    if type(almostFinal[i][j]) != str:
                        for k in range(len(almostFinal[i][j])):
                            final[i].append(almostFinal[i][j][k])
                    else:
                        final[i].append(almostFinal[i][j])
            print("Final: ", final)
            return final
        else:
            #for now same line as other case, if it stays can take it out of if/else
            possibilities = []
            for i in range(numItems):
                possibilities.append(getAllPossibilities(parentReqs.items[i]))
            #final really is just one of the things that ends up in possibilities
            #possibilities is a list of (list of lists of strings)
            #we really just want one of the lists of strings as each element in final
            final = []
            for i in range(len(possibilities)):
                for j in range(len(possibilities[i])):
                    final.append(possibilities[i][j])
            return final







    # #base case is when the list is all strings:
    # numItems = len(parentReqs.items)
    # numString = 0
    # for i in range(numItems):
    #   if type(parentReqs.items[i]) == str:
    #       numString += 1
    # if numString == numItems:
    #   #BASE CASE
    #   if parentReqs.isAnded:
    #       return parentReqs.items[:] 
    #   else:
    #       possibilities = []
    #       for i in range(numItems):
    #           possibilities.append([parentReqs.items[i]])
    #       return possibilities
    # else:
    #   #let's think about the case where we have 2 strings and 1 reqList




        


#if i were doing it by hand, I'd look at the smallest guy first, at some point somebody has
#to be just made up of strings. Then if it's and, we return a list of all those. 
#if it's or, we return several lists of the individuals. 
