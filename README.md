# SATsolver #
SAT solver for a school project. Two methods were implemented. Both take a CNF in DIMACS format as input and return the result in DIMACS format.

## Algorithms
Two different algorithms were implemented with different options and upgrades. Below is a table comparing both of them.

Upgrade | DPLL | CDCL
------- | ---- | ----
pureLiterals | :heavy_check_mark: | :x:
[2WL](#two-watched-lists-2wl "Goto 2WL") | :x: | :heavy_check_mark:
[UIP](#unit-implication-point-uip "Goto UIP") | :x: | :heavy_check_mark:
[Heuristics](#heuristics "Goto Heuristics") | :x: | :heavy_check_mark:
[Resets](#resets "Goto Resets") | :x: | :heavy_check_mark:

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
* `-d` or `--dpll`: use `DPLL` instead of `CDCL` (suggested to use with `-l`)
* `-l` or `--pureLiterals`: runs `DPLL` without checking for pure literals (in practice this usually greatly increases performance)
* `-r` or `--resets`: runs `CDCL` without resets
* `-h` or `--heuristics`: runs `CDCL` without heuristics (chooses the first available variable when making a decision)
* `-p:` or `--resetPoint=`: takes an integer and determines the starting point for reset depth

Some problems may be solved faster with different settings, thus these options are available. Take note that changing settings concerning pure literals only works for `DPLL` algorithm, while the rest of the options only change the behaviour of the `CDCL` algorithm.

## Setting up tests
Several `Python` files are included that generate SAT problems. Those are n-queens, dominating set, colourability, hamiltonian path, hamiltonian cycle and sudoku.

## Benchmarking
Below are some benchmarks using both algorithms with different options. All test files can be found in [Examples](Examples). If the solution was not found within 5 minutes, the program was stopped (marked with :x: in the table).

Input file | DPLL | DPLL -l | CDCL | CDCL -r
---------- | ---- | ------- | ---- | -------
sudoku_hard | 0.06s | 0.04s | 0.04s | 0.04s
sudoku_easy | 0.03s | 0.02s | 0.041s | 0.04s
15-queens | 0.25s | 0.25s | 1.01s | 1.02s
20-queens | 32.35s | 32.25s | 8.08s | 8.27s
33-queens | :x: | :x: | 1.55s | :x:
col1 | 0.00s | 0.00s | 0.00s | 0.00s
col3 | :x: | :x: | 0.99s | 1.00s
domset | 0.00s | 0.00s | 0.00s | 0.00s
hamiltonian path 1 | :x: | :x: | 55.73s | 76.00s
hamiltonian path 2 | 179.29s | 175.28s | 0.10s | 0.10s
hamiltonian path 3 | :x: | :x: | 1.02s | 14.89s
hamiltonian cycle 1 | :x: | :x: | 2.63s | 4.32s
