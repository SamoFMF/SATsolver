# SATsolver #
SAT solver for a school project. Two methods were implemented. Both take a CNF in DIMACS format as input and return the result in a custom format. If a problem is unsatisfiable the program outputs `0`, else it outputs literals seperated by spaces.

## Additional instructions
Instructions also state that a problem should be added to the repository that can be solved within a minute and demonstrates the strengths of the algorithm. I'd suggest two problems, the first is a [Hamiltonian path](Examples/hamiltonian_path/g1/sat.txt). This specific example pushes the algorithm to nearly a minute of execution time. The second is the [33-queens](Examples/nqueens/sat33.txt) problem which was not solved by any iteration of my solvers until `Resets` were added. This means that it demonstrates the strengths of the algorithm quite well.

## Algorithms
Two different algorithms were implemented with different options and upgrades. Below is a table comparing both of them.

Upgrade | DPLL | CDCL
------- | ---- | ----
pureLiterals | :heavy_check_mark: | :x:
[2WL](#two-watched-lists-2wl "Go to 2WL") | :x: | :heavy_check_mark:
[UIP](#unit-implication-point-uip "Go to UIP") | :x: | :heavy_check_mark:
[Heuristics](#heuristics "Go to Heuristics") | :x: | :heavy_check_mark:
[Resets](#resets "Go to Resets") | :x: | :heavy_check_mark:

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
Running the program can be done with the following command-line command:

`python mysolver.py <inputfilename> <outputfilename> [options]`

Available options to change the behaviour of the algorithm are:
* `-d` or `--dpll`: use `DPLL` instead of `CDCL` (suggested to use with `-l`)
* `-l` or `--pureLiterals`: runs `DPLL` without checking for pure literals (in practice this usually greatly increases performance)
* `-r` or `--resets`: runs `CDCL` without resets
* `-h` or `--heuristics`: runs `CDCL` without heuristics (chooses the first available variable when making a decision)
* `-p:` or `--resetPoint=`: takes an integer and determines the starting point for reset depth
* `-c` or `--conflicts`: prints the number of conflicts found while solving the problem
* `-t` or `--time`: prints time used to solve the problem (including read and write times unlike the [table](#benchmarking "Go to Benchmarking") below)

Some problems may be solved faster with different settings, thus these options are available. Take note that changing settings concerning pure literals only works for `DPLL` algorithm, while the rest of the options only change the behaviour of the `CDCL` algorithm.

## Setting up tests
Several `Python` files are included that generate SAT problems. Those are [n-queens](Examples/nqueens/nqueens2sat.py), [dominating set](Examples/domset/domset2sat.py "Open source code"), [colourability](Examples/colourability/col2sat.py "Open source code"), [hamiltonian path](Examples/hamiltonian_path/hampath2sat.py "Open source code"), [hamiltonian cycle](Examples/hamiltonian_cycle/hamcycle2sat.py "Open source code") and [sudoku](Examples/sudoku/sudoku2sat.py "Open source code").

A file [checkResult](Examples/checkResult.py "Open source code") was also added which checks the validity of the result (in the format of the output of implemented algorithms) compared to the CNF formula given in DIMACS format. It can be run with:

`python Examples/checkResult.py <input CNF name> <result file name>`

## Benchmarking
Below are some benchmarks using both algorithms with different options. All test files can be found in [Examples](Examples "Go to Examples"). If the solution was not found within 5 minutes, the program was stopped (marked with :x: in the table).

Input file | DPLL | DPLL -l | CDCL | CDCL -r
---------- | ---- | ------- | ---- | -------
[sudoku_easy](Examples/sudoku/s2/sat.txt) | [0.03s](Examples/sudoku/s2/sol3.txt) | [0.02s](Examples/sudoku/s2/sol4.txt) | [0.04s](Examples/sudoku/s2/sol1.txt) | [0.04s](Examples/sudoku/s2/sol2.txt)
[sudoku_hard](Examples/sudoku/s1/sat.txt) | [0.06s](Examples/sudoku/s1/sol3.txt) | [0.04s](Examples/sudoku/s1/sol4.txt) | [0.04s](Examples/sudoku/s1/sol1.txt) | [0.04s](Examples/sudoku/s1/sol2.txt)
[15-queens](Examples/nqueens/sat15.txt) | [0.25s](Examples/nqueens/sol153.txt) | [0.25s](Examples/nqueens/sol154.txt) | [1.01s](Examples/nqueens/sol151.txt) | [1.02s](Examples/nqueens/sol152.txt)
[20-queens](Examples/nqueens/sat20.txt) | [32.35s](Examples/nqueens/sol203.txt) | [32.25s](Examples/nqueens/sol204.txt) | [8.08s](Examples/nqueens/sol201.txt) | [8.27s](Examples/nqueens/sol202.txt)
[33-queens](Examples/nqueens/sat33.txt) | :x: | :x: | [1.55s](Examples/nqueens/sol331.txt) | :x:
[colourability 1](Examples/colourability/g1/sat2.txt) | [0.00s](Examples/colourability/g1/sol3.txt) | [0.00s](Examples/colourability/g1/sol4.txt) | [0.00s](Examples/colourability/g1/sol1.txt) | [0.00s](Examples/colourability/g1/sol2.txt)
[colourability 2](Examples/colourability/g2/sat5.txt) | :x: | :x: | [0.99s](Examples/colourability/g2/sol1.txt) | [1.00s](Examples/colourability/g2/sol2.txt)
[dominating set](Examples/domset/g1/sat3.txt) | [0.00s](Examples/domset/g1/sol3.txt) | [0.00s](Examples/domset/g1/sol4.txt) | [0.00s](Examples/domset/g1/sol1.txt) | [0.00s](Examples/domset/g1/sol2.txt)
[hamiltonian path 1](Examples/hamiltonian_path/g1/sat.txt) | :x: | :x: | [55.73s](Examples/hamiltonian_path/g1/sol1.txt) | [76.00s](Examples/hamiltonian_path/g1/sol2.txt)
[hamiltonian path 2](Examples/hamiltonian_path/g2/sat.txt) | [179.29s](Examples/hamiltonian_path/g2/sol3.txt) | [175.28s](Examples/hamiltonian_path/g2/sol4.txt) | [0.10s](Examples/hamiltonian_path/g2/sol1.txt) | [0.10s](Examples/hamiltonian_path/g2/sol2.txt)
[hamiltonian path 3](Examples/hamiltonian_path/g3/sat.txt) | :x: | :x: | [1.02s](Examples/hamiltonian_path/g3/sol1.txt) | [14.89s](Examples/hamiltonian_path/g3/sol2.txt)
[hamiltonian cycle 1](Examples/hamiltonian_cycle/g1/sat.txt) | [49.06s](Examples/hamiltonian_cycle/g1/sol3.txt) | [49.19s](Examples/hamiltonian_cycle/g1/sol4.txt) | [0.08s](Examples/hamiltonian_cycle/g1/sol1.txt) | [0.08s](Examples/hamiltonian_cycle/g1/sol2.txt)
[hamiltonian cycle 2](Examples/hamiltonian_cycle/g2/sat.txt) | :x: | :x: | [2.62s](Examples/hamiltonian_cycle/g2/sol1.txt) | [4.68s](Examples/hamiltonian_cycle/g2/sol2.txt)
