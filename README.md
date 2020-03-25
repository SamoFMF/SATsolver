# SATsolver
SAT solver for a school project. Two methods were implemented. Both take a CNF in DIMACS format as input and return the result in DIMACS format.

## DPLL
Uses the basic `DPLL` algorithm to solve the SAT problem.

## CDCL
An implementation of the `CDCL` algorithm with the following additions:
* 2WL
* UIP
* Heuristics
* Resets

### Two watched lists (2WL)
Instead of keeping track of every literal in the clause, we only watch two of them. If one of them becomes `False` and the other one is not `True`, we try to find a new literal that is not `False` to watch. This way, we will always recognize if the clause is `False`, but might not know if it satisfied.

### Unit Implication Point (UIP)
When a conflict occurs the basic `CDCL` algorithm calculates the new clause by backtracking through the implication graph until the root of the decision level is reached. This is not always necessary though, as there may be a point on the path that is dominating the conflict vertex. Such a point is called a UIP. If one or more UIPs exist, the one closest to the conflict point is chosen.

### Heuristics
When the algorithm needs to make a decision (i.e. pick a variable and its value that is not forced), it chooses the variable that occurs in the most clauses. More specifically it chooses the most common literal (or atleast a literal on the same level of the binary tree as the optimal available literal).

### Resets
Resets are used to stop the algorithm from searching too deep when wrong decisions were made.

The algorithm resets when the depth of atleast `100` is reached and starts over. The depth needed to restart is then multiplied by `1.1`. Heuristic values may have changed in that time (because of new clauses), therefor the algorithm might traverse down a different path.

## Running the program
Running the program can be done through the terminal:

`python mysolver.py inputfile.txt outputfile.txt`

Additionally we can add several options to change the behaviour of the algorithm:
* `-d` or `--dpll`: use `DPLL` instead of `CDCL` (all other options are ignored in this case)
* `-r` or `--resets`: runs `CDCL` without resets
* `-h` or `--heuristics`: runs `CDCL` without heuristics (chooses the first available variable when making a decision)
* `-p:` or `--resetPoint=`: takes an integer and determines the starting point for reset depth

Some problems may be solved faster with different settings, thus these options are available.
