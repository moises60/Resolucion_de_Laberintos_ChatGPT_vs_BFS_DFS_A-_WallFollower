from collections import deque

def solve_maze_bfs(maze, start, goal):
    """
    Argumentos:
        maze (Maze): Laberinto con atributos .rows, .cols y .grid (0 pasillo, 1 pared)
        start (tuple): (row, col) de inicio
        goal (tuple): (row, col) de meta
    Descripción:
        Aplica Búsqueda en Amplitud (BFS) para hallar una ruta desde 'start' hasta 'goal'
        Devuelve una lista de celdas que marcan esa ruta, o None si no hay camino
    Salidas:
        path (list of (row, col)): Ruta desde start hasta goal, o None si no hay ruta
    """
    start_row, start_col = start
    goal_row, goal_col = goal
    
    # Si inicio o meta son paredes, no hay camino
    if maze.grid[start_row][start_col] == 1 or maze.grid[goal_row][goal_col] == 1:
        return None
    
    queue = deque([start])
    visited = {start}
    came_from = {start: None}
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  

    while queue:
        current = queue.popleft()
        if current == goal:
            # Reconstruir la ruta
            return reconstruct_path(came_from, start, goal)
        
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Verificar que no sea pared y que esté dentro de límites
            if 0 <= nr < maze.rows and 0 <= nc < maze.cols:
                if maze.grid[nr][nc] == 0: 
                    neighbor = (nr, nc)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        queue.append(neighbor)
    
    # no hay meta
    return None

def reconstruct_path(came_from, start, goal):
    """
    Reconstruye la ruta guardada en 'came_from' tras llegar a 'goal'
    """
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
