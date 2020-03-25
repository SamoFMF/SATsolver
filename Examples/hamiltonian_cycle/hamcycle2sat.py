# # Graph colourability to SAT

import sys
from collections import defaultdict

#############################################################################
# HAMILTONIAN CYCLE TO SAT                                                  #
#                                                                           #
# x_{i,r} ... i-th node is the r-th node in the path | 0<=i<=n-1, 0<=r<=k-1 #
#                                                                           #
# These variables will be represented in DIMACS by:                         #
#   x_{i,r} = i*k + r + 1                                                   #
#############################################################################

def hampath2sat(f):
    line = f.readline()
    while line[0] == "c":
        line = f.readline()
    _,_,n,m = line.rstrip("\n").split()
    n = int(n)
    m = int(m)
    nodes = defaultdict(set) # Dictionary of nodes
    for _ in range(m):
        _, i, j = f.readline().rstrip("\n").split()
        i = int(i)
        j = int(j)
        if j<i:
            i,j = j,i
        elif i == j:
            continue
        nodes[i].add(j)
    # We can't calculate the number of clauses, because the formula
    # would be wrong if there were multiple inputs of the same edge
    # in the input or vertices connected to themselves
    numOfDisj = n**2 * (n+3) // 2
    cnf = ""
    # There is atleast 1 node in every position
    for r in range(n):
        for i in range(n):
            x = i*n + r + 1
            cnf += f"{x} "
        cnf += "0\n"
    # Atmost 1 node per position on the path
    for r in range(n):
        for i in range(n):
            for j in range(i+1, n):
                x = i*n + r + 1
                y = j*n + r + 1
                cnf += f"-{x} -{y} 0\n"
    # Every node is in atleast 1 position
    for i in range(n):
        for r in range(n):
            x = i*n + r + 1
            cnf += f"{x} "
        cnf += "0\n"
    # If edges are not connected, they cannot be adjacent in the path
    for i in range(n):
        for j in range(i+1, n):
            if j+1 in nodes[i+1]:
                # Nodes are connected
                continue
            for r in range(n-1):
                x = i*n + r + 1
                y = j*n + r+1 + 1
                cnf += f"-{x} -{y} 0\n"

                x = i*n + r+1 + 1
                y = j*n + r + 1
                cnf += f"-{x} -{y} 0\n"

                numOfDisj += 2
            cnf += f"-{i*n + n} -{j*n + 1} 0\n"
            cnf += f"-{i*n + 1} -{j*n + n} 0\n"
            numOfDisj += 2
    return f"p cnf {n**2} {numOfDisj}\n" + cnf

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
    cnf = hampath2sat(inFile)
    outFile.write(cnf)
    inFile.close()
    outFile.close()

if __name__ == "__main__":
    main()