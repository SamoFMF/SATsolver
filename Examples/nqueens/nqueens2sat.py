# n-kraljic
# Prevedba n-kraljic na SAT v DIMACS

import sys

def nq2sat(n):
    cnf = "c n-kraljic preveden na SAT v DIMACS formatu\n"
    cnf += f"p cnf {n*n} {2*n + n*n*(n-1) + (n-1)*n*(2*n-1)//3}\n"
    # V vsaki vrstici vsaj 1 kraljica - takih disjunkcij je n
    for row in range(n):
        for col in range(n):
            x = row*n + col + 1
            cnf += str(x) + " "
        cnf += "0\n"
    # V vsakem stolpcu vsaj 1 kraljica - n disjunkcij
    for col in range(n):
        for row in range(n):
            x = row*n + col + 1
            cnf += str(x) + " "
        cnf += "0\n"
    # V vsaki vrstici največ 1 kraljica - n*n*(n-1)//2 disjunkcij
    for row in range(n):
        for col1 in range(n):
            for col2 in range(col1+1, n):
                x1 = row*n + col1 + 1
                x2 = row*n + col2 + 1
                cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
    # V vsakem stolpcu največ 1 kraljica - n*n*(n-1)//2 disjunkcij
    for col in range(n):
        for row1 in range(n):
            for row2 in range(row1+1, n):
                x1 = row1*n + col + 1
                x2 = row2*n + col + 1
                cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
    # Na vsaki diagonali največ 1 kraljica - (n-1)*n*(n+1)//6 + (n-2)*(n-1)*n//6 = (n-1)*n*(2*n-1)//6
    for d in range(n):
        for f1 in range(n-d):
            for f2 in range(f1+1, n-d):
                x1 = (d+f1)*n + f1 + 1
                x2 = (d+f2)*n + f2 + 1
                cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
    for d in range(n-1):
        for f1 in range(n-1-d):
            for f2 in range(f1+1, n-1-d):
                x1 = f1*n + (d+1+f1) + 1
                x2 = f2*n + (d+1+f2) + 1
                cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
    # Na vsaki antidiagonali največ 1 kraljica - (n-1)*n*(n+1)//6 + (n-2)*(n-1)*n//6 = (n-1)*n*(2*n-1)//6
    for d in range(n):
        for f1 in range(d+1):
            for f2 in range(f1+1, d+1):
                x1 = f1*n + (d-f1) + 1
                x2 = f2*n + (d-f2) + 1
                cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
    for d in range(n-1):
        for f1 in range(n-1-d):
            for f2 in range(f1+1, n-1-d):
                x1 = (d+1+f1)*n + (n-1-f1) + 1
                x2 = (d+1+f2)*n + (n-1-f2) + 1
                cnf += "-" + str(x1) + " -" + str(x2) + " 0\n"
    return cnf


def main():
    if len(sys.argv) > 2:
        n = int(sys.argv[1])
        outFile = open(sys.argv[2], "w")
    elif len(sys.argv) == 2:
        n = int(sys.argv[1])
        outFile = sys.stdout
    else:
        n = int(sys.stdin.readline())
        outFile = sys.stdout
    cnf = nq2sat(n)
    outFile.write(cnf)
    outFile.close()

if __name__ == "__main__":
    main()