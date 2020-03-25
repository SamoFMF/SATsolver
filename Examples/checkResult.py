# Check result of CNF (both in DIMACS)

import sys

def solve(inCNF, inRES):
    with open(inRES) as f:
        res = {i for i in f.readline().rstrip("\n").split()}
    with open(inCNF) as f:
        line = f.readline()
        while line[0] == "c":
            line = f.readline()
        _,_,_,numOfClauses = line.split()
        for _ in range(int(numOfClauses)):
            line = f.readline().rstrip("\n")
            for i in line.split():
                if i in res:
                    break
            else:
                print("FAIL", line)
                break
        else:
            print("DONE")

def main():
    solve(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()