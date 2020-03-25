# Graph colourability to SAT

import sys

###############################################################
# k-COLOURABILITY TO SAT                                      #
#                                                             #
# x_{i,r} ... i-th node is of colour r | 0<=i<=n-1, 0<=r<=k-1 #
#                                                             #
# These variables will be represented in DIMACS by:           #
#   x_{i,r} = i*k + r + 1                                     #
###############################################################

def col2sat(f, k):
    '''Takes a file f containing a graph in DIMACS format
    and positive integer k and transforms it into a
    k-colourability SAT problem.'''
    line = f.readline()
    while line[0] == "c":
        line = f.readline()
    _,_,n,m = line.rstrip("\n").split()
    n = int(n)
    m = int(m)
    numOfDisj = k + n + n*k*(k-1)//2 + m*k # number of disjunction clauses
    cnf = f"p cnf {n*k} {numOfDisj}\n"
    # For every colour there is atleast 1 node || k clauses
    # This can be avoided if we only care if there is an l-colourability
    # for some l<=k, because that means that the graph is also k-colourable
    for r in range(k):
        for i in range(n):
            x = i*k + r + 1
            cnf += str(x) + " "
        cnf += "0\n"
    # Every node has atleast 1 colour || n clauses
    for i in range(n):
        for r in range(k):
            x = i*k + r + 1
            cnf += str(x) + " "
        cnf += "0\n"
    # Every node has atmost 1 colour || n*k*(k-1)//2 clauses
    for i in range(n):
        for r in range(k):
            for s in range(r+1, k):
                x = i*k + r + 1
                y = i*k + s + 1
                cnf += "-" + str(x) + " -" + str(y) + " 0\n"
    # Every connected pair must have different colours || m*k clauses
    for _ in range(m):
        _, i, j = f.readline().rstrip("\n").split()
        i = int(i) - 1
        j = int(j) - 1
        for r in range(k):
            x = i*k + r + 1
            y = j*k + r + 1
            cnf += "-" + str(x) + " -" + str(y) + " 0\n"
    return cnf

def main():
    if len(sys.argv) > 3:
        k = int(sys.argv[1])
        inFile = open(sys.argv[2])
        outFile = open(sys.argv[3], "w")
    elif len(sys.argv) == 3:
        k = int(sys.argv[1])
        inFile = open(sys.argv[2])
        outFile = sys.stdout
    elif len(sys.argv) == 2:
        k = int(sys.argv[1])
        inFile = sys.stdin
        outFile = sys.stdout
    else:
        k = int(sys.stdin.readline())
        inFile = sys.stdin
        outFile = sys.stdout
    cnf = col2sat(inFile, k)
    outFile.write(cnf)
    inFile.close()
    outFile.close()

if __name__ == "__main__":
    main()