# Logic in computer science
# Homework: Implementing a SAT Solver

import sys
from time import time

__all__ = ['solve']

def dpll(cnf, numOfVars=729, usePureLiterals=True):
    varVals = [None]*numOfVars
    solved = 0
    
    while True:
        if len(cnf) == 0:
            return varVals
        
        unitClauses = dict() # a dictionary of all clauses that only have a single literal
        pureLiterals = dict() # dictionary of type name:val for every pure literal
        notPureLiterals = set() # list of literals that are not pure
        clausesToRemove = set() # clauses to be removed

        for i, orList in enumerate(cnf):
            # Traverse through cnf searching for empty disjunctions, unit clauses and pure literals
            if len(orList) == 0:
                return None # empty disjunction = FALSE => conjunction is also FALSE
            elif len(orList) == 1:
                # Found a literal
                l = orList[0]
                if abs(l) in unitClauses:
                    # It can either be that the clause evaluates into True
                    # Or it can be that l is the negation of the literal in
                    # unitClauses and the problem is NONSAT
                    # In both cases it will be handled later
                    continue
                elif abs(l) in pureLiterals:
                    del pureLiterals[abs(l)]
                varVals[solved] = l # add literal to output
                solved += 1
                unitClauses[abs(l)] = l>0 # add literal to the dict of unit clauses
                clausesToRemove.add(i) # add clause to clauses to be removed
            elif usePureLiterals:
                for l in orList:
                    # Traverse through the literals in the disjunction
                    # Searching for pure literals
                    absl = abs(l)
                    if absl in unitClauses or absl in notPureLiterals:
                        # Literal is either a unit clause ... don't care if it is also pure
                        # or we already not it's not pure
                        continue
                    elif absl in pureLiterals:
                        if (l>0 and pureLiterals[absl][0]) or (l<=0 and not pureLiterals[absl][0]): # equality can be ignored, since variable names are != 0
                            pureLiterals[absl][1].append(i)
                        else:
                            del pureLiterals[absl]
                            notPureLiterals.add(absl)
                    else:
                        pureLiterals[absl] = (l>0, [i])
        
        if len(clausesToRemove) == len(cnf):
            # Every clause evaluated into True => the whole formula is true
            return varVals
        elif len(unitClauses) == 0 and len(pureLiterals) == 0:
            # There are no unit clauses and/or pure literals
            # We must choose a variable and its value
            # First break out of the while loop
            break

        # For pure literals: add the clauses containing them
        # to the set clausesToRemove, because we can evaluate
        # all of those disjunctions into True (= remove them)
        for l in pureLiterals:
            if pureLiterals[l][0]:
                varVals[solved] = l
            else:
                varVals[solved] = -l
            solved += 1
            for i in pureLiterals[l][1]:
                clausesToRemove.add(i)
        
        # We now remove all clauses whose indices are contained
        # in the set clausesToRemove, while traversing the list
        # of the remaining clauses and checking if they contain
        # any of the literals from unit clauses
        cnfNew = [None]*(len(cnf)-len(clausesToRemove))
        j = 0 # index for traversing through cnfNew
        for i in range(len(cnf)):
            if i in clausesToRemove:
                continue
            else:
                newOr = []
                for l in cnf[i]:
                    absl = abs(l)
                    if absl in unitClauses:
                        if (l>0 and unitClauses[absl]) or (l<=0 and not unitClauses[absl]):
                            # Clause evaluates into True
                            break
                        else:
                            # Remove literal from clause
                            continue
                    else:
                        newOr.append(l)
                else:
                    # Loop ended - clause remains
                    cnfNew[j] = newOr
                    j += 1
        cnf = cnfNew[:j]
    
    # Take the first literal ... try to solve if it is True and False
    i1 = cnf[0][0]
    d = dpll(cnf + [[i1]], numOfVars-solved) or dpll(cnf + [[-i1]], numOfVars-solved)
    if d:
        varVals[solved:] = d
        return varVals
    else:
        return d

def createCNF(inFile):
    with open(inFile) as f:
        line = f.readline()
        while line[0] == "c":
            line = f.readline()
        _,_,numOfVars,numOfClauses = line.split()
        cnf = [None] * int(numOfClauses)
        for i in range(len(cnf)):
            line = f.readline()
            cnf[i] = [int(j) for j in line.split()[:-1]]
    return cnf, int(numOfVars)

def solve(inFile, outFile, usePureLiterals=True):
    cnf, numOfVars = createCNF(inFile)
    t = time()
    solution = dpll(cnf, numOfVars, usePureLiterals)
    print(time()-t)
    print("SATISFIED" if solution else "UNSATISFIABLE")
    with open(outFile, "w") as f:
        if solution:
            f.write(" ".join(map(str,solution)))
        else:
            f.write("0")

def main():
    t = time()
    solve(sys.argv[1], sys.argv[2])
    print(time()-t)

if __name__ == "__main__":
    main()