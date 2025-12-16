import time  # Used to measure execution time of each algorithm

def bfs(maze, start, end):
    """
    Breadth-First Search (BFS)
    Explores the maze level by level and guarantees the shortest path
    in an unweighted grid.
    """
    t0 = time.time()  # Start timing

    rows, cols = len(maze), len(maze[0])
    queue = [start]                 # Queue for BFS
    visited = {start: None}         # Stores parent of each visited node
    head = 0                        # Pointer to simulate queue pop
    nodes_expanded = 0              # Counts explored nodes

    while head < len(queue):
        y, x = queue[head]
        head += 1
        nodes_expanded += 1

        # Stop search if goal is reached
        if (y, x) == end:
            break

        # Explore neighboring cells (Up, Down, Left, Right)
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y + dy, x + dx

            # Check bounds, walkable cell, and not visited
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0 and (ny, nx) not in visited:
                queue.append((ny, nx))
                visited[(ny, nx)] = (y, x)  # Save parent

    path = reconstruct_path(visited, end)
    t1 = time.time()  # End timing

    return path, nodes_expanded, (t1 - t0) * 1000  # Return results


def dfs(maze, start, end):
    """
    Depth-First Search (DFS)
    Explores as deep as possible before backtracking.
    Does NOT guarantee shortest path.
    """
    t0 = time.time()

    rows, cols = len(maze), len(maze[0])
    stack = [start]                 # Stack for DFS
    visited = {start: None}
    nodes_expanded = 0

    while stack:
        y, x = stack.pop()
        nodes_expanded += 1

        if (y, x) == end:
            break

        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0 and (ny, nx) not in visited:
                stack.append((ny, nx))
                visited[(ny, nx)] = (y, x)

    path = reconstruct_path(visited, end)
    t1 = time.time()

    return path, nodes_expanded, (t1 - t0) * 1000


def dijkstra(maze, start, end):
    """
    Uniform Cost Search (Dijkstra)
    Finds the shortest path by expanding the lowest-cost node first.
    """
    t0 = time.time()

    rows, cols = len(maze), len(maze[0])
    heap = [(0, start)]             # (cost, node)
    visited = {start: None}
    costs = {start: 0}
    nodes_expanded = 0

    while heap:
        heap.sort()                 # Sort by cost
        cost, (y, x) = heap.pop(0)
        nodes_expanded += 1

        if (y, x) == end:
            break

        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0:
                new_cost = cost + 1
                if (ny, nx) not in costs or new_cost < costs[(ny, nx)]:
                    costs[(ny, nx)] = new_cost
                    heap.append((new_cost, (ny, nx)))
                    visited[(ny, nx)] = (y, x)

    path = reconstruct_path(visited, end)
    t1 = time.time()

    return path, nodes_expanded, (t1 - t0) * 1000


def astar(maze, start, end):
    """
    A* Search Algorithm
    Uses cost + heuristic (Manhattan distance) to guide the search.
    """
    t0 = time.time()

    rows, cols = len(maze), len(maze[0])
    open_list = [(heuristic(start, end), 0, start)]  # (f, g, node)
    visited = {start: None}
    g_score = {start: 0}
    nodes_expanded = 0

    while open_list:
        open_list.sort()             # Sort by f-score
        _, g, current = open_list.pop(0)
        nodes_expanded += 1

        if current == end:
            break

        y, x = current
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)

            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0:
                tentative_g = g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    open_list.append((f, tentative_g, neighbor))
                    visited[neighbor] = current

    path = reconstruct_path(visited, end)
    t1 = time.time()

    return path, nodes_expanded, (t1 - t0) * 1000


def heuristic(a, b):
    """
    Manhattan distance heuristic
    Used by A* to estimate distance to the goal.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(visited, end):
    """
    Reconstructs the path from end node to start node
    using the visited dictionary.
    """
    if end not in visited:
        return []

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = visited[current]

    return path[::-1]  # Reverse path
