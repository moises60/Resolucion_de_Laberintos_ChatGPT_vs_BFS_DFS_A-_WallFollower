import pygame

class Maze:
    def __init__(self):
        self.grid = []
        self.rows = 0
        self.cols = 0

    def load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            line = f.readline().strip()
            self.rows, self.cols = map(int, line.split())
            self.grid = []
            for _ in range(self.rows):
                row_data = f.readline().strip().split()
                row_ints = [int(value) for value in row_data]
                self.grid.append(row_ints)

    def generate_random(self, rows, cols):
        import random
        self.rows = rows
        self.cols = cols
        self.grid = []
        for r in range(rows):
            row_list = []
            for c in range(cols):
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    row_list.append(1) 
                else:
                    row_list.append(0 if random.random() < 0.8 else 1)
            self.grid.append(row_list)

    def draw(self, screen, tile_size):
        """
        Argumentos:
            screen (pygame.Surface): Superficie de Pygame donde se dibuja el laberinto
            tile_size (int): Tamaño (en píxeles) de cada celda
        Descripción:
            Recorre self.grid y dibuja un rectángulo para cada celda:
            - 1 (pared): color gris
            - 0 (pasillo): color blanco
        Salidas:
            Ninguna
        """
        # Definimos colores básicos
        color_wall = (120, 120, 120)   # gris
        color_path = (220, 220, 220)   # gris claro

        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row][col]
                x = col * tile_size
                y = row * tile_size

                if cell_value == 1:
                    color = color_wall
                else:
                    color = color_path

                pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))


    def draw_at(self, screen, tile_size, offset_x, offset_y):
        """
        Argumentos:
            screen (pygame.Surface): Superficie de Pygame donde se dibuja el laberinto
            tile_size (int): Tamaño en píxeles para cada celda (versión "mini")
            offset_x (int): Desplazamiento en el eje X para dibujar el laberinto
            offset_y (int): Desplazamiento en el eje Y para dibujar el laberinto
        Descripción:
            Dibuja la cuadrícula del laberinto en la posición (offset_x, offset_y) de la pantalla,
            usando el tile_size especificado.
        """
        color_wall = (120, 120, 120)  # gris
        color_path = (220, 220, 220)  # gris claro

        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row][col]
                x = offset_x + col * tile_size
                y = offset_y + row * tile_size

                if cell_value == 1:
                    color = color_wall
                else:
                    color = color_path

                pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
