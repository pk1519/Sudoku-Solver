import tkinter as tk
from tkinter import messagebox, ttk
import random


def is_safe(grid, row, col, num, grid_size):
    """Check if it's safe to place num in grid[row][col]."""
    for i in range(grid_size):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    subgrid_size = int(grid_size ** 0.5)
    box_row, box_col = subgrid_size * (row // subgrid_size), subgrid_size * (col // subgrid_size)
    for i in range(box_row, box_row + subgrid_size):
        for j in range(box_col, box_col + subgrid_size):
            if grid[i][j] == num:
                return False

    return True


def solve_sudoku(grid, grid_size):
    """Solve Sudoku using backtracking."""
    empty_cell = find_empty(grid, grid_size)
    if not empty_cell:
        return True

    row, col = empty_cell
    for num in range(1, grid_size + 1):
        if is_safe(grid, row, col, num, grid_size):
            grid[row][col] = num
            if solve_sudoku(grid, grid_size):
                return True
            grid[row][col] = 0

    return False


def find_empty(grid, grid_size):
    """Find an empty cell in the grid."""
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == 0:
                return (i, j)
    return None


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#1e1e2e")  # Dark background color
        self.root.state('zoomed')  # Open in full screen

        self.grid_size_var = tk.IntVar(value=9)
        self.cells = []

        # Initialize the GUI components
        self.create_grid_size_option()
        self.create_grid()
        self.create_buttons()

    def create_grid_size_option(self):
        label = tk.Label(self.root, text="Select Grid Size:", font=('Verdana', 14, 'bold'), fg="#f4e8c1", bg="#1e1e2e")
        label.grid(row=0, column=0, columnspan=3)

        size_options = ttk.Combobox(self.root, textvariable=self.grid_size_var, values=[2, 3, 4, 6, 8, 9],
                                     state="readonly")
        size_options.grid(row=0, column=3, columnspan=3)
        size_options.bind("<<ComboboxSelected>>", self.on_grid_size_change)

    def create_grid(self):
        self.clear_grid()

        grid_size = self.grid_size_var.get()
        self.cells = [[None for _ in range(grid_size)] for _ in range(grid_size)]

        for i in range(grid_size):
            for j in range(grid_size):
                entry = tk.Entry(self.root, width=5, font=('Comic Sans MS', 16), justify='center', bd=3, relief="flat",
                                 bg="#f4e8c1", fg="#1e1e2e", validate="key",
                                 validatecommand=(self.root.register(self.validate_input), '%P'))
                entry.grid(row=i + 2, column=j, padx=4, pady=4, sticky='nsew')
                entry.bind("<FocusIn>", self.on_entry_focus)
                self.cells[i][j] = entry

        for i in range(grid_size):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i + 2, weight=1)

    def create_buttons(self):
        grid_size = self.grid_size_var.get()

        button_style = {'font': ('Verdana', 12), 'width': 20, 'bg': '#495057', 'fg': '#f4e8c1', 'relief': 'raised'}

        random_button = tk.Button(self.root, text="Get Puzzle", command=self.generate_random_sudoku,
                                  **button_style)
        random_button.grid(row=grid_size + 2, column=0, columnspan=3, pady=10, padx=5)

        solve_button = tk.Button(self.root, text="Solve Puzzle", command=self.solve_puzzle, **button_style)
        solve_button.grid(row=grid_size + 2, column=3, columnspan=2, pady=10, padx=5)

        show_solution_button = tk.Button(self.root, text=" AI Solver ", command=self.animate_solution, **button_style)
        show_solution_button.grid(row=grid_size + 2, column=5, columnspan=2, pady=10, padx=5)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid, **button_style)
        clear_button.grid(row=grid_size + 3, column=2, columnspan=3, pady=10, padx=5)

    def on_grid_size_change(self, event=None):
        self.clear_grid()
        self.create_grid()

    def clear_grid(self):
        for cell in self.cells:
            for entry in cell:
                if entry is not None:
                    entry.destroy()

        self.cells = []

    def get_grid_values(self):
        grid_size = self.grid_size_var.get()
        grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                value = self.cells[i][j].get()
                if value == '' or not value.isdigit() or not (1 <= int(value) <= grid_size):
                    row.append(0)
                else:
                    row.append(int(value))
            grid.append(row)
        return grid

    def set_grid_values(self, grid):
        grid_size = self.grid_size_var.get()
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] != 0:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(grid[i][j]))

    def validate_input(self, value):
        """Allow only a single digit from 1 to 9 as valid input."""
        if value == '':
            return True
        if value.isdigit() and 1 <= int(value) <= 9:
            return True
        return False

    def on_entry_focus(self, event):
        """Optional: Handle focus event for entry fields if needed."""
        pass

    def solve_puzzle(self):
        grid = self.get_grid_values()
        grid_size = self.grid_size_var.get()

        if solve_sudoku(grid, grid_size):
            self.set_grid_values(grid)
            messagebox.showinfo("Congratulations!", "You solved the Sudoku!")
        else:
            messagebox.showinfo("Try Again", "This Sudoku puzzle is incorrect. Try again!")

    def animate_solution(self):
        grid = self.get_grid_values()
        grid_size = self.grid_size_var.get()

        if self.solve_sudoku_animated(grid, grid_size):
            messagebox.showinfo("Solved!", "The Sudoku puzzle is solved.")
        else:
            messagebox.showinfo("Error", "No solution exists for this Sudoku puzzle.")

    def solve_sudoku_animated(self, grid, grid_size):
        empty_cell = find_empty(grid, grid_size)
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, grid_size + 1):
            if is_safe(grid, row, col, num, grid_size):
                grid[row][col] = num
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].insert(0, str(num))
                self.cells[row][col].update()
                self.root.after(100)

                if self.solve_sudoku_animated(grid, grid_size):
                    return True
                grid[row][col] = 0
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].update()
                self.root.after(100)

        return False

    def generate_random_sudoku(self):
        grid_size = self.grid_size_var.get()
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        self.fill_grid(grid, grid_size)
        self.remove_numbers(grid, grid_size)
        self.set_grid_values(grid)

    def fill_grid(self, grid, grid_size):
        """Fill the grid using backtracking."""
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] == 0:
                    num_list = list(range(1, grid_size + 1))
                    random.shuffle(num_list)
                    for num in num_list:
                        if is_safe(grid, i, j, num, grid_size):
                            grid[i][j] = num
                            if self.fill_grid(grid, grid_size):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    def remove_numbers(self, grid, grid_size, difficulty=0.5):
        """Remove numbers to create a puzzle with a given difficulty."""
        num_to_remove = int(grid_size * grid_size * difficulty)
        while num_to_remove > 0:
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            if grid[row][col] != 0:
                grid[row][col] = 0
                num_to_remove -= 1


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

#pyinstaller --onefile --windowed sudoku.py
