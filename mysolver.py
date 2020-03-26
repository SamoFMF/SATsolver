# Logic in computer science
# Project: Implementing a SAT Solver

import sys
from getopt import getopt
from dpll import solve as solvedpll
from cdcl import solve as solvecdcl

def main():
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    options, _ = getopt(sys.argv[3:], "drp:hl", ["dpll", "resets", "resetPoint=", "heuristics", "pureLiterals"])

    # Default values
    dpll = False
    resets = True
    resetPoint = 100
    heuristics = True
    usePureLiterals = True

    # Update options
    for o,v in options:
        if o == "--dpll" or o == "-d":
            dpll = True
        elif o == "--resets" or o == "-r":
            resets = False
        elif o == "--resetPoint" or o == "-p":
            resetPoint = int(v)
        elif o == "-h" or o == "-heuristics":
            heuristics = False
        else:
            usePureLiterals = False
    
    # Create CNF
    if dpll:
        # DPLL
        print("Running DPLL algorithm.")
        solvedpll(inFile, outFile, usePureLiterals)
    else:
        print(f"Running CDCL algorithm {'with' if resets else 'without'} resets, {'with a reset point at ' + str(resetPoint) + ', ' if resets else ''}and {'with' if heuristics else 'without'} heuristics.")
        solvecdcl(inFile, outFile, resets, resetPoint, heuristics)

if __name__ == "__main__":
    main()