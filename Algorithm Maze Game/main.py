from maze_generator import generate_maze
from algorithms import bfs, dfs, dijkstra, astar
from visualizer import MazeApp

# Entry point of the program
# Creates the Maze application and starts the GUI
if __name__ == "__main__":
    MazeApp(generate_maze, bfs, dfs, dijkstra, astar).run()
