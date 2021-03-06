# Dominating set to SAT

import sys

def dom2sat(f, k, outFile):
    line = f.readline()
    while line[0] == "c":
        line = f.readline()
    _,_,n,m = line.rstrip("\n").split()
    n = int(n)
    m = int(m)
    nodes = {i+1: [] for i in range(n)} # Dictionary of nodes
    for _ in range(m):
        _, i, j = f.readline().rstrip("\n").split()
        i = int(i)
        j = int(j)
        if i == j:
            continue
        nodes[i].append(j)
        nodes[j].append(i)
    numOfDisj = k + k*n*(n+k-2)//2 + n
    outFile.write(f"p cnf {n*k} {numOfDisj}\n")
    # Atleast 1 node in every position
    for r in range(k):
        cnf = ""
        for i in range(n):
            x = i*k + r + 1
            cnf += str(x) + " "
        cnf += "0\n"
        outFile.write(cnf)
    # No node can be in rth and sth position in dominating set
    for i in range(n):
        for r in range(k):
            for s in range(r+1,k):
                x1 = i*k + r + 1
                x2 = i*k + s + 1
                # cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
                outFile.write(f"-{x1} -{x2} 0\n")
    # Atmost 1 node can be in rth position
    for r in range(k):
        print(r)
        for i in range(n):
            for j in range(i+1, n):
                x1 = i*k + r + 1
                x2 = j*k + r + 1
                # cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
                outFile.write(f"-{x1} -{x2} 0\n")
    # Every node needs to be in the dominating set or be
    # connected to atleast 1 node in the dominating set
    idx = 0
    for i in nodes:
        if len(nodes[i]) == 0:
            x = (i-1)*k + idx + 1
            idx += 1
            # cnf += str(x) + " 0\n"
            outFile.write(f"{x} 0\n")
        else:
            cnf = ""
            for r in range(k):
                x = (i-1)*k + r + 1
                cnf += str(x) + " "
                for j in nodes[i]:
                    x = (j-1)*k + r + 1
                    cnf += str(x) + " "
            cnf += "0\n"
            outFile.write(cnf)

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
    dom2sat(inFile, k, outFile)
    inFile.close()
    outFile.close()

if __name__ == "__main__":
    main()