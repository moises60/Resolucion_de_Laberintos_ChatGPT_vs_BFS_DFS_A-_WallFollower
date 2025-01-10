import pygame

class Robot:
    """
    Representa un robot dentro de un laberinto
    """

    def __init__(self, start_row=1, start_col=1, color=(255, 0, 0)):
        """
        Argumentos:
            start_row (int): Fila inicial del robot
            start_col (int): Columna inicial del robot
            color (tuple): Color (RGB) del robot
        Descripción:
            Inicializa la posición y color del robot
        """
        self.row = start_row
        self.col = start_col
        self.color = color

    def draw(self, screen, tile_size):
        """
        Argumentos:
            screen (pygame.Surface): Superficie de Pygame donde dibujamos al robot
            tile_size (int): Tamaño de cada celda en píxeles
        Descripción:
            Dibuja el robot como un círculo en el centro de la celda (row, col)
        """
        center_x = self.col * tile_size + tile_size // 2
        center_y = self.row * tile_size + tile_size // 2
        radius = tile_size // 4
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)

    def move(self, maze, drow, dcol):
        """
        Argumentos:
            maze (Maze): Laberinto en el que se mueve el robot
            drow (int): Desplazamiento en filas (p.e. -1, 0, 1)
            dcol (int): Desplazamiento en columnas (p.e. -1, 0, 1)
        Descripción:
            Mueve el robot en la dirección indicada, si la celda destino es un pasillo (0)
            Evita que atraviese paredes (1).
        """
        new_row = self.row + drow
        new_col = self.col + dcol

        # Comprobar límites del laberinto
        if 0 <= new_row < maze.rows and 0 <= new_col < maze.cols:
            # Comprobar si la celda destino no es pared
            if maze.grid[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col
