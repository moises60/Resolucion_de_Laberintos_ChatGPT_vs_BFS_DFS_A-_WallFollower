def follow_wall(maze, start, goal, side="right"):
    """
    Argumentos:
        maze (Maze): Laberinto con .grid, .rows, .cols
        start (tuple): (row, col) de inicio
        goal (tuple): (row, col) de meta
        side (str): "right" o "left", define de qué lado seguimos la pared
    Descripción:
        Implementa la regla de la pared (derecha o izquierda)
        Devuelve la ruta (lista de celdas) hasta la meta, o None si no se encuentra
    Salidas:
        path (list of (row, col)) o None
    """
    # Si start o goal son paredes, no hay nada que hacer
    if maze.grid[start[0]][start[1]] == 1 or maze.grid[goal[0]][goal[1]] == 1:
        return None

    # Inicializamos la orientación (ej. si el robot mira "hacia abajo")
    # Puedes escoger otra orientación inicial. 
    # up=(−1,0), right=(0,1), down=(1,0), left=(0,−1).
    direction = (0, 1)  # mirando derecha

    current = start
    path = [current]

    # Para prevenir bucles infinitos, definimos un límite de iteraciones
    max_steps = maze.rows * maze.cols * 10

    for _ in range(max_steps):
        if current == goal:
            return path

        # Determinamos la secuencia de giros en función de "side"
        # Si side="right": primero intentamos girar a la derecha, 
        # si no, seguimos recto, si no, giramos izq, si no, atra
        # ka lógica inversa si side="left".

        possible_directions = get_directions_in_priority(direction, side)

        moved = False
        for d in possible_directions:
            nr = current[0] + d[0]
            nc = current[1] + d[1]
            if (0 <= nr < maze.rows) and (0 <= nc < maze.cols):
                if maze.grid[nr][nc] == 0:  # pasillo
                    direction = d
                    current = (nr, nc)
                    path.append(current)
                    moved = True
                    break
        
        if not moved:
            # Si no pudimos movernos en ninguna dirección (encerrado) / pasa en los ultimos niveles
            return None
    
    # Si superamos max_steps, asumimos que no hallamos la meta
    return None

def get_directions_in_priority(current_direction, side="right"):
    """
    Retorna una lista de direcciones (drow, dcol) en orden de prioridad 
    según la regla de la pared (derecha o izquierda)
    Ejemplo (side="right"), si la dirección actual es (0,1) => "derecha", 
    el orden de prioridad es: 
       1) down (1,0)
       2) right (0,1)
       3) up (-1,0)
       4) left (0,-1)
    """
    # Direcciones base
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    dirs = [up, right, down, left]

    # Ubicar el índice de la dirección actual en 'dirs'
    idx = dirs.index(current_direction)

    if side == "right":
        # Prioridad: girar derecha -> recto -> izquierda -> atrás
        # "girar derecha" significa idx+1 (mod 4)
        # "recto" => idx
        # "izquierda" => idx-1 (mod 4)
        # "atrás" => idx+2 (mod 4)
        priority = [
            dirs[(idx + 1) % 4],  # derecha
            dirs[idx],           # recto
            dirs[(idx - 1) % 4], # izquierda
            dirs[(idx + 2) % 4]  # atrás
        ]
    else:
        # side == "left"
        # Prioridad: girar izquierda -> recto -> derecha -> atrás
        priority = [
            dirs[(idx - 1) % 4], # izquierda
            dirs[idx],           # recto
            dirs[(idx + 1) % 4], # derecha
            dirs[(idx + 2) % 4]  # atrás
        ]

    return priority
