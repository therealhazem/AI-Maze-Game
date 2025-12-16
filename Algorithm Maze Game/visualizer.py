import tkinter as tk
from tkinter import ttk

class MazeApp:
    """
    Graphical User Interface for the Maze Solver
    """

    def __init__(self, generate_maze, bfs, dfs, dijkstra, astar):
        # Maze generator and search algorithms
        self.generate_maze = generate_maze
        self.algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "Uniform Cost Search": dijkstra,
            "A*": astar
        }

        self.maze = []
        self.path = []
        self.cell = 10  # Size of each cell

        # Store previous results for comparison
        self.prev_steps = None
        self.prev_time = None

        # Main window setup
        self.root = tk.Tk()
        self.root.title("Algorithms Maze Game")
        self.root.configure(bg="#D6ECFA")

        # Title label
        tk.Label(
            self.root,
            text="Algorithms Maze Game",
            font=("Helvetica", 22, "bold"),
            bg="#D6ECFA",
            fg="#1B3C59"
        ).pack(pady=15)

        # Canvas for maze drawing
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=2)
        self.canvas.pack()

        # Controls frame
        controls = tk.Frame(self.root, bg="#D6ECFA")
        controls.pack(pady=10)

        style = {
            "bg": "#FFF3B0",
            "fg": "#1B3C59",
            "font": ("Arial", 10, "bold"),
            "activebackground": "#FFE066"
        }

        # Buttons and algorithm selector
        tk.Button(controls, text="Generate Maze", command=self.new_maze, **style).pack(side=tk.LEFT, padx=5)

        self.algo_box = ttk.Combobox(controls, values=list(self.algorithms.keys()), state="readonly")
        self.algo_box.current(0)
        self.algo_box.pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Solve", command=self.solve, **style).pack(side=tk.LEFT, padx=5)

        # Statistics display
        stats = tk.Frame(self.root, bg="#D6ECFA")
        stats.pack(pady=10)

        self.steps_lbl = tk.Label(stats, text="Steps: -", font=("Arial",11,"bold"), bg="#D6ECFA")
        self.steps_lbl.pack(side=tk.LEFT, padx=20)

        self.time_lbl = tk.Label(stats, text="Time: - ms", font=("Arial",11,"bold"), bg="#D6ECFA")
        self.time_lbl.pack(side=tk.LEFT, padx=20)

    def run(self):
        """Starts the Tkinter main loop"""
        self.root.mainloop()

    def new_maze(self):
        """Generates a new maze and resets statistics"""
        self.maze = self.generate_maze()
        self.path = []
        self.prev_steps = None
        self.prev_time = None

        self.steps_lbl.config(text="Steps: -", fg="black")
        self.time_lbl.config(text="Time: - ms", fg="black")

        self.draw()

    def solve(self):
        """Solves the maze using the selected algorithm"""
        if not self.maze:
            return

        start = (0, 1)
        end = (len(self.maze) - 1, len(self.maze[0]) - 2)
        algo = self.algorithms[self.algo_box.get()]

        path, _, time_ms = algo(self.maze, start, end)
        steps = len(path)

        # Color comparison logic
        if self.prev_steps is None:
            steps_color = "black"
            time_color = "black"
        else:
            steps_color = "green" if steps <= self.prev_steps else "red"
            time_color = "green" if time_ms <= self.prev_time else "red"

        self.steps_lbl.config(text=f"Steps: {steps}", fg=steps_color)
        self.time_lbl.config(text=f"Time: {time_ms:.2f} ms", fg=time_color)

        self.prev_steps = steps
        self.prev_time = time_ms
        self.path = path

        self.draw()

    def draw(self):
        """Draws the maze, path, start and end points"""
        self.canvas.delete("all")
        rows, cols = len(self.maze), len(self.maze[0])
        self.canvas.config(width=cols*self.cell, height=rows*self.cell)

        # Draw maze grid
        for y in range(rows):
            for x in range(cols):
                color = "#1B3C59" if self.maze[y][x] == 1 else "white"
                self.canvas.create_rectangle(
                    x*self.cell, y*self.cell,
                    (x+1)*self.cell, (y+1)*self.cell,
                    fill=color, outline="gray"
                )

        # Draw solution path
        for y, x in self.path:
            self.canvas.create_rectangle(
                x*self.cell, y*self.cell,
                (x+1)*self.cell, (y+1)*self.cell,
                fill="#4CAF50"
            )

        # Draw start and end cells
        self.canvas.create_rectangle(1*self.cell, 0, 2*self.cell, self.cell, fill="#FF6B6B")
        self.canvas.create_rectangle(
            (cols-2)*self.cell, (rows-1)*self.cell,
            (cols-1)*self.cell, rows*self.cell,
            fill="#FF6B6B"
        )
