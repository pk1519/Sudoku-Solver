
Here's a detailed README for your Sudoku Solver project. This file will guide users through setup, usage, and additional information about the project's features and functionality.

# Sudoku Solver
A graphical Sudoku Solver built using Python and Tkinter. This app allows users to input custom Sudoku puzzles or generate random ones and provides solutions via a backtracking algorithm. Users can solve puzzles manually or let the AI solver fill in the grid step-by-step, showing animated solutions.

# Features

Customizable Grid Sizes: Supports a variety of grid sizes, including 2x2, 3x3, 4x4, 6x6, 8x8, and the traditional 9x9.
Random Puzzle Generation: Generates a new puzzle with adjustable difficulty for each grid size.
Instant and Animated Solutions: Solve puzzles instantly or use the AI solver to view the solution step-by-step.
User-Friendly GUI: Built with Tkinter, featuring a modern design, dark mode, and intuitive controls.

# Requirements
Python 3.x
Tkinter library (usually included with Python)

# How to Use
Select Grid Size: Choose your preferred grid size from the dropdown menu at the top.
Generate Puzzle: Click Get Puzzle to create a new random Sudoku puzzle.
Solve Puzzle:
Solve Puzzle: Instantly fills in the solution for the puzzle.
AI Solver: Solves the puzzle one step at a time, animating the process.
Clear Grid: Clears all cells to allow for a new puzzle or manual input.

# Code Overview
is_safe: Checks if a number can be placed in a specific cell.
solve_sudoku: Uses a backtracking algorithm to solve the puzzle.
find_empty: Finds the next empty cell in the grid.
SudokuGUI: Manages the user interface and interactions, including grid creation, input validation, and puzzle-solving.

# Packaging
To create a standalone executable using PyInstaller, run below code in cmd

pyinstaller --onefile --windowed sudoku.py

# Contact
email-priyanshu00909@gmail.com
