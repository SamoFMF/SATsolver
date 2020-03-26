# Logic in computer science
# Homework: Implementing a SAT Solver
# CDCL with:
#   - 2WL
#   - UIP
#   - heap
#   - resets

import sys
from myheap import heapify, decreaseKey
from time import time

# CONSTANTS
SAT = "SATISFIED" # Satisfied
UNSAT = "UNSATISFIED" # Unsatisfied
UNIT = "UNITCLAUSE" # Unit clause
UNRES = "UNRESOLVED" # Unresolved
CONFLICT = "CONFLICT" # Conflict

class Var:
    def __init__(self, i):
        self.i = i
        self.val = 0.5 # unassigned
        self.a = None # antecedent ... previous in tree
        self.d = -1 # decision level
        self.watchedP = [] # Clauses in which the variable is watched and is not negated
        self.watchedN = [] # Clauses in which the negated value of the variable is watched
        self.numId = -1 # Specifies when the variable was added (which in line)
        self.heapVal = 0
        self.heapPos = None
        self.heap = None
        self.containedIn = [0, 0] # Contained in clauses as [positive, negated]

    def __repr__(self):
        return f'|{self.i}|'
    
    def addWatched(self, l, c, pos):
        if l<0:
            self.watchedN.append((c, pos))
        else:
            self.watchedP.append((c, pos))
    
    def updateVariableL(self, l, a, d, numId):
        '''Update variable where input is given as a literal.'''
        self.val = 1 if l>0 else 0
        self.a = a
        self.d = d
        self.numId = numId
    
    def updateVariableV(self, v, a, d, numId):
        '''Update variable where input is given as a value.'''
        self.val = v
        self.a = a
        self.d = d
        self.numId = numId
    
    def initHeapVal(self):
        self.heapVal = max(self.containedIn)
    
    def updateHeapVal(self, l):
        if l>0:
            self.containedIn[0] += 1
        else:
            self.containedIn[1] += 1
        newVal = max(self.containedIn)
        if newVal > self.heapVal:
            self.heapVal = newVal
            decreaseKey(self.heap, self.heapPos)

    def swapValue(self):
        self.val = 1-self.val
    
    def reset(self):
        self.val = 0.5
        self.a = None
        self.d = -1
        self.numId = -1

class Clause:
    def __init__(self, w, vs):
        self.vs = vs # Dictionary of variables
        self.w = w # List of literals
        self.watched = [None, None]
    
    def __repr__(self):
        # return f"<{['-'+i[1] if i[0] else i[1] for i in self.w]}, {self.watched}>"
        return "<" + str(self.w) + ", " + str(self.watched) + ">"
    
    def getValue(self, l):
        return self.vs[l].val if l>0 else 1-self.vs[-l].val

    def initWatched(self):
        # Initiate 2-watched list
        for i,l in enumerate(self.w):
            if self.getValue(l) == 0:
                # Literal evaluates to False
                continue
            else:
                x = self.vs[l] if l>0 else self.vs[-l]
                self.watched[0] = l
                x.addWatched(l, self, 0)
                break
        else:
            # Every literal evaluates to False
            return UNSAT
        for j in range(len(self.w)-1, i, -1):
            l = self.w[j]
            if self.getValue(l) == 0:
                # Literal evaluates to False
                continue
            else:
                # Found an unwatched literal that doesn't eval to False
                x = self.vs[l] if l>0 else self.vs[-l]
                self.watched[1] = l
                x.addWatched(l, self, 1)
                break
        else:
            # Didn't find a non-false literal, meaning the
            # clause is unit ... set the second watched
            # literal to be any other literal than the
            # first watched, unless the clause has 1 literal
            if len(self.w) == 1:
                # Set both to watch the same literal, but DON'T add it to
                # the list of watched clauses twice
                l = self.w[0]
                self.watched[1] = l
                return SAT if self.getValue(l) == 1 else UNIT
            else:
                # Unit clause with more than 1 literal
                l = self.w[(i+1)%len(self.w)]
                x = self.vs[l] if l>0 else self.vs[-l]
                self.watched[1] = l
                x.addWatched(l, self, 1)
                if self.getValue(self.watched[0]) == 1 or self.getValue(l) == 1:
                    return SAT
                else:
                    return UNIT
        # Found 2 different non-False literals to watch
        # Check if either of them is True
        if self.getValue(self.watched[0]) == 1 or self.getValue(self.watched[1]) == 1:
            return SAT
        else:
            return UNRES
    
    def updateWatched(self, pos):
        l1 = self.watched[pos] # The watched literal that is now False
        l2 = self.watched[1-pos] # The other watched literal
        l2v = self.getValue(l2)
        if l2v == 1:
            # The second watched literal is True
            # Therefore there is no point in changing
            # either watched literal
            return SAT, True
        else:
            # Try to find an unwatched literal that is not False
            for l in self.w:
                if l == l1 or l == l2:
                    # Currently watched literal
                    # OR the other watched literal
                    continue
                else:
                    lv = self.getValue(l)
                    if lv == 0:
                        # l is False
                        continue
                    else:
                        # Found a new literal to watch
                        self.watched[pos] = l
                        self.vs[l].addWatched(l, self, pos) if l>0 else self.vs[-l].addWatched(l, self, pos)
                        if lv == 1:
                            return SAT, False
                        else:
                            return UNRES, False
            if l2v == 0:
                # All literals in the clause are False
                return CONFLICT, True
            else:
                # Literal 2 is unasigned
                # Unit clause
                return UNIT, True

def readInput(inFile):
    with open(inFile) as f:
        line = f.readline()
        while line[0] == "c":
            line = f.readline()
        _,_,numOfVars,numOfClauses = line.split()
        variables = {i:Var(i) for i in range(1, int(numOfVars)+1)} # create dictionary of variables
        cnf = [None] * int(numOfClauses)
        for i in range(len(cnf)):
            w = []
            for l in map(int,f.readline().split()[:-1]):
                if l>0:
                    variables[l].containedIn[0] += 1
                else:
                    variables[-l].containedIn[1] += 1
                w.append(l)
            cnf[i] = Clause(w, variables)
    return cnf, variables

class CDCL:
    def __init__(self, cnf, variables, resets=True, resetPoint=100, heuristics=False):
        self.cnf = cnf # List of all disjunctions
        self.variables = variables # Dictionary of all variables
        self.dl = 0 # Decision level
        self.solved = 0 # Variables solved
        self.atLevel = [[]] # Variables solved at each decision level
        self.Q = [] # The queue of variables to still be considered
        self.heap = None
        self.resetPoint = resetPoint
        self.alreadyUsed = set() # Set of already used starting variables
        self.startNumOfClauses = len(self.cnf) # Used in the end to get the number of conflicts

        # Choose correct solver
        if resets:
            self.makeDecision = self.makeDecisionReset
        else:
            self.makeDecision = self.makeDecisionNoReset
        self.heuristics = heuristics
        if self.heuristics:
            self.pickBranchingVariable = self.pickBranchingVariableHeap
        else:
            self.pickBranchingVariable = self.pickBranchingVariableNoHeap
    
    def setVarValueL(self, l, c):
        # Set value of literal l in clause c
        # so that it evaluates into True
        x = self.variables[l] if l>0 else self.variables[-l]
        x.updateVariableL(l, c, self.dl, self.solved)

        # This solved a variable ... increase 'solved'
        self.solved += 1

        # Variable was solved at level 'dl'
        self.atLevel[self.dl].append(x)

        # A variables value was changed
        # Watched clauses should be updated
        # Put variable in the queue
        self.Q.append(x)
    
    def setVarValueV(self, x, v, c):
        # Set value of literal l in clause c
        # so that it evaluates into True
        x.updateVariableV(v, c, self.dl, self.solved)

        # This solved a variable ... increase 'solved'
        self.solved += 1

        # Variable was solved at level 'dl'
        self.atLevel[self.dl].append(x)

        # A variables value was changed
        # Watched clauses should be updated
        # Put variable in the queue
        self.Q.append(x)
    
    def updateWatched(self, x):
        # Get the pointer to the appropriate watch list
        # If x.val=1, clauses containing (Not x) will evaluate it into False
        # Otherwise clauses containing x will evaluate it into False
        watched = x.watchedN if x.val == 1 else x.watchedP
        watchedNew = []
        for i, (c, pos) in enumerate(watched):
            # Traverse the clauses that watch the value
            status, keep = c.updateWatched(pos) # Update the clause
            if status == CONFLICT:
                # We found a conflict
                watched[:i] = watchedNew # Update watched list
                return True, c
            elif status == UNIT:
                # Found a unit clause
                # Set the value of the variable
                # in the non-watched position
                self.setVarValueL(c.watched[1-pos], c)

                # Add element to watchedNew
                watchedNew.append((c, pos))
            elif keep:
                # SAT without changes
                watchedNew.append((c, pos))
            else:
                # SAT or UNRES, both with changes to the watched literal
                continue
        if x.val == 1:
            x.watchedN = watchedNew
        else:
            x.watchedP = watchedNew
        return False, None

    def initUnitPropagation(self):
        # Initial propagation, when the queue is empty
        # Check if there are any unit clauses
        for c in self.cnf:
            status = c.initWatched()
            if status == CONFLICT:
                # Conflict before any decisions were made
                # Problem is unsatisfiable
                return True
            elif status == UNIT:
                # Unit clause
                # Set the value of the watched literal
                # so that it evaluates into True
                l = c.watched[0]
                self.setVarValueL(l, c)
            else:
                # Clause is unresolved ... nothing to do
                continue
        if self.solved < len(self.variables):
            # Problem is not solved yet ... init heapq
            self.heap = [None] * (len(self.variables) - self.solved)
            i = 0
            for x in self.variables.values():
                if x.val != 0.5:
                    continue
                self.heap[i] = x
                x.heap = self.heap
                x.heapPos = i
                x.initHeapVal()
                i += 1
            heapify(self.heap)
        return False
    
    def unitPropagation(self):
        # Propagate while 'Q' is not empty
        i = 0
        while i < len(self.Q):
            x = self.Q[i]
            status, c = self.updateWatched(x)
            if status:
                # Found a conflict
                # Clear the queue
                # Report the clause
                self.Q = []
                return True, c
            i += 1
        self.Q = []
        return False, None
    
    def pickBranchingVariableNoHeap(self):
        for x in self.variables.values():
            if x.val == 0.5:
                if len(x.watchedN) > len(x.watchedP):
                    return x, 0
                else:
                    return x, 1
        return None, -1

    def pickBranchingVariableHeap(self):
        '''Pick an unasigned variable.'''
        for x in self.heap:
            if x.val == 0.5:
                if x.containedIn[1] > x.containedIn[0]:
                    return x, 0
                else:
                    return x, 1
        return None, -1
    
    def containsLevelD(self, w, d):
        '''Returns literal if w contains literals
        of decision level d with literal.a != None.'''
        for l in w:
            x = l[1]
            if x.d == d and x.a is not None:
                return x
        return None
    
    def resolution(self, w1, w2, x):
        # TODO - premisli, ce res vedno tako?
        wNew = []
        seen = {x.i, -x.i}
        for l in w1:
            if l not in seen:
                wNew.append(l)
                seen.add(l)
        for l in w2:
            if l not in seen:
                wNew.append(l)
                seen.add(l)
        return wNew
    
    def chooseNextVar(self, w):
        maxx = None
        maxv = -2
        counter = 0
        for l in w:
            x = self.variables[l] if l>0 else self.variables[-l]
            if x.d == self.dl:
                counter += 1
                if x.numId > maxv:
                    maxv = x.numId
                    maxx = x
        if counter <= 1:
            return None
        else:
            return maxx
    
    def getLevel(self, w):
        if len(w) == 1:
            return 0
        else:
            max1 = -1
            max2 = -1
            for l in w:
                x = self.variables[l] if l>0 else self.variables[-l]
                if x.d > max1:
                    max1, max2 = x.d, max1
                elif x.d > max2:
                    max2 = x.d
            return max2
    
    def conflictAnalysis(self, w):
        wL = [i for i in w]
        x = self.chooseNextVar(wL)
        while x:
            wL = self.resolution(wL, x.a.w, x)
            x = self.chooseNextVar(wL)
        return wL, self.getLevel(wL)
    
    def assertLevel(self, beta):
        for d in range(self.dl, beta, -1):
            for x in self.atLevel[d]:
                x.reset()
                self.solved -= 1
            del self.atLevel[d]
        self.dl = beta
    
    def backtrack(self, beta):
        for d in range(self.dl, beta-1, -1):
            for x in self.atLevel[d]:
                x.reset()
                self.solved -= 1
            del self.atLevel[d]
    
    def reset(self):
        self.dl -= 1
        self.assertLevel(0)
        self.resetPoint *= 1.1
    
    def makeDecisionNoReset(self):
        self.dl += 1
        self.atLevel.append([])
        x, v = self.pickBranchingVariable()
        self.setVarValueV(x, v, None)
        return False
    
    def makeDecisionReset(self):
        self.dl += 1
        if self.dl > self.resetPoint:
            self.reset()
            return True
        self.atLevel.append([])
        x, v = self.pickBranchingVariable()
        self.setVarValueV(x, v, None)
        return False
    
    def solve(self):
        '''Solve without resets.'''
        if self.initUnitPropagation():
            # There was a conflict before any decisions were made
            return UNSAT
        while self.solved < len(self.variables):
            if len(self.Q) == 0 and self.makeDecision():
                # The queue is empty ... we made a decision
                # Decision level exceeded resetPoint
                # We reset the values and start again
                continue
            status, c = self.unitPropagation()
            if status:
                # Found a conflict: conflict analysis
                wL, beta = self.conflictAnalysis(c.w)
                if beta < 0:
                    # All variables in wL are unasigned or were propagated
                    # before any decisions were made, adding wL to
                    # conjunction would not change anything
                    return UNSAT
                else:
                    # At level beta, wL is a unit clause
                    self.assertLevel(beta)

                    # Add wL to cnf and initialize it
                    c = Clause(wL, self.variables)
                    self.cnf.append(c)
                    status = c.initWatched()
                    if status == CONFLICT:
                        # This should never happen
                        return UNSAT
                    elif status == UNIT:
                        # Added a unit clause ... propagate the appropriate variable
                        self.setVarValueL(c.watched[0], c)

                        if self.heuristics:
                            # Update heap and priority values
                            for l in wL:
                                x = self.variables[l] if l>0 else self.variables[-l]
                                if x.heap:
                                    x.updateHeapVal(l)
                    elif status == UNSAT:
                        # Clause is not satisfiable
                        # Usually means that there is only 1 literal in it
                        # and its variable has already been asigned in a way
                        # that evaluates the literal to False
                        return UNSAT
                    else:
                        # This should never happen
                        print("wL is NOT unit!")
                        continue
        return SAT

def solve(inFile, outFile, resets=True, resetPoint=100, heuristics=True):
    cnf, var = readInput(inFile)
    sat = CDCL(cnf, var, resets, resetPoint, heuristics)
    t = time()
    x = sat.solve()
    print(time()-t)
    print(f"{len(sat.cnf)-sat.startNumOfClauses} conflicts")
    print(x)
    with open(outFile, "w") as f:
        if x == UNSAT:
            f.write("0")
        else:
            f.write(" ".join(map(str, [i.i if i.val == 1 else -i.i for i in sat.variables.values()])))

def main():
    t = time()
    solve(sys.argv[1], sys.argv[2])
    print(time()-t)

if __name__ == "__main__":
    main()