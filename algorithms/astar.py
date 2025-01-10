import heapq

def solve_maze_astar(maze, start, goal):
    """
    Argumentos:
        maze (Maze): Laberinto con .rows, .cols y .grid (0 = pasillo, 1 = pared)
        start (tuple): (row, col) de inici
        goal (tuple): (row, col) de meta
    Descripción:
        Aplica el algoritmo A* para hallar una ruta desde 'start' hasta 'goal'
        Utiliza la distancia de Manhattan como heurística, y asume coste uniforme (1) por paso
    Salidas:
        path (list of (row, col)): Ruta si se encuentra, o None si no existe
    """
    (start_row, start_col) = start
    (goal_row, goal_col) = goal

    # Si inicio o meta son paredes, nada que hacer
    if maze.grid[start_row][start_col] == 1 or maze.grid[goal_row][goal_col] == 1:
        return None

    frontier = []
    # Cada elemento en 'frontier' será (f, (r, c)), donde f = g + h
    # g = coste real desde start, h = heurística Manhattan
    start_f = 0 + manhattan_distance(start, goal)
    heapq.heappush(frontier, (start_f, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while frontier:
        current_f, current = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.rows and 0 <= nc < maze.cols:
                if maze.grid[nr][nc] == 0:  # pasillo
                    new_cost = cost_so_far[current] + 1  # costo 1 por paso
                    neighbor = (nr, nc)
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + manhattan_distance(neighbor, goal)
                        heapq.heappush(frontier, (priority, neighbor))
                        came_from[neighbor] = current
    return None

def manhattan_distance(a, b):
    """
    Distancia de Manhattan entre dos celdas (row1, col1) y (row2, col2)
    """
    (r1, c1) = a
    (r2, c2) = b
    return abs(r1 - r2) + abs(c1 - c2)

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
