# SudokuSolver
 Sudoku Solver

Usage example:

```python
puzzle = [
    [0,0,2,0,0,4,0,7,5],
    [0,7,5,0,0,0,0,8,0],
    [4,0,0,7,5,0,3,0,0],
    [0,0,0,0,0,0,8,0,3],
    [0,5,0,4,0,0,0,1,0],
    [3,1,0,0,0,6,0,0,0],
    [5,8,0,9,4,1,0,3,2],
    [7,4,0,5,0,2,0,0,8],
    [9,0,1,0,0,0,0,0,6]
]

solver = sudoku_solver()
solver.new_puzzle(puzzle)
solved = solver.solve()
print(solved)
```
