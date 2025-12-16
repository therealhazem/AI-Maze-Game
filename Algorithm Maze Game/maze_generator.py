import random

def generate_maze(width=41, height=41):
    """
    Generates a random maze using recursive backtracking.
    1 = wall, 0 = path
    """

    # Ensure odd dimensions for proper maze carving
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1

    # Initialize maze filled with walls
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        """
        Recursive carving function that creates passages
        """
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y+dy][x+dx] = 0
                maze[ny][nx] = 0
                carve(nx, ny)

    # Start carving from position (1,1)
    maze[1][1] = 0
    carve(1,1)

    # Create entrance and exit
    maze[0][1] = 0
    maze[height-1][width-2] = 0

    # Add random openings to create multiple solutions
    for _ in range((width * height) // 10):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        maze[y][x] = 0

    return maze
