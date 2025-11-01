## Sudoku Solver (VBA)

A lightweight Sudoku solver written in VBA for Microsoft Excel. This project was originally built as a personal challenge and a small gift for my grandfather. The solver uses a combination of candidate elimination and a recursive backtracking algorithm to complete standard 9×9 Sudoku puzzles.

### Files
- `Sudoku Solver.bas`: VBA module containing the solver logic (candidate generation, backtracking, helper macros).
- `Sudoku Solver.xlsm`: A macro-enabled workbook that provides the interface for running the solver.

### Algorithm Overview
- The solver begins by determining all valid candidates for each empty cell, removing numbers already found in the same row, column or 3×3 block.
- It automatically fills in any cells that have a single valid candidate.
- If multiple possibilities remain, it applies a recursive depth-first search (backtracking) to test each candidate until the puzzle is solved.

While a linear programming approach can solve Sudoku puzzles more efficiently, this project was about exploring recursion and algorithmic problem-solving. It was a rewarding way to connect with my grandfather and showcase how programming can bring logic to life.