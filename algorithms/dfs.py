def solve_maze_dfs(maze, start, goal):
    """
    Argumentos:
        maze (Maze): Laberinto con .rows, .cols, .grid (0 = pasillo, 1 = pared)
        start (tuple): (row, col) inicio
        goal (tuple): (row, col) meta
    Descripción:
        Aplica DFS para buscar una ruta desde 'start' hasta 'goal'
    Salidas:
        path (list of (row, col)) o None: La ruta si se encontró, o None
    """
    stack = [start]
    visited = {start}
    came_from = {start: None}
    directions = [(-1,0),(1,0),(0,-1),(0,1)] 

    while stack:
        current = stack.pop() 
        if current == goal:
            return reconstruct_path(came_from, start, goal)

        r, c = current
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < maze.rows and 0 <= nc < maze.cols:
                if maze.grid[nr][nc] == 0:  # pasillo
                    neighbor = (nr, nc)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        stack.append(neighbor)
    
    return None 

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
