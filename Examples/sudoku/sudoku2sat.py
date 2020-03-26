# Takes a string input of a sudoku
# 0 ... empty field
# input should be of the form:
# v11 v12 v13 ... v19
# v21 v22 v23 ... v29
# ...
# v91 v92 v93 ... v99

import sys

def createSudoku(inFile, outFile):
    unitClauses = ""
    num = 0
    for i in range(9):
        line = inFile.readline()
        for j, val in enumerate([int(k) for k in line.split()]):
            if val > 0:
                unitClauses += str(81*i + 9*j + val) + " 0\n"
                num += 1
    with open("sudokuTemplate.txt") as f:
        with open(outFile, "w") as g:
            g.write(f'p cnf 729 {num+11988}\n')
            g.write(unitClauses)
            for line in f:
                g.write(line)

def main():
    if len(sys.argv) > 2:
        inFile = sys.argv[1]
        outFile = sys.argv[2]
    else:
        inFile = sys.stdin
        outFile = sys.argv[1]
    createSudoku(inFile, outFile)

if __name__ == "__main__":
    main()