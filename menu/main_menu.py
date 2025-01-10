import pygame
import os
from labyrinth.maze import Maze
from menu.level_selector import list_levels

def run_menu_scene(screen, clock, levels):
    """
    Argumentos:
        screen (pygame.Surface): Ventana principal de Pygame
        clock (pygame.time.Clock): Reloj de Pygame para regular FPS
        levels (list of str): Lista de archivos de nivel disponibles
    Descripción:
        Dibuja un menú en pantalla donde el usuario puede seleccionar
        uno de los niveles con flechas o clic. Devuelve el nombre
        del archivo seleccionado, o None si el usuario sale
    Salidas:
        selected_level (str o None): El nombre de archivo elegido, o None si cancela
    """
    font = pygame.font.Font(None, 36)

    # Cargamos todos los laberintos en memoria para su vista previa
    previews = {}
    for lvl in levels:
        m = Maze()
        m.load_from_file(os.path.join("data/mazes/", lvl))
        previews[lvl] = m

    selected_index = 0
    running_menu = True
    selected_level = None

    while running_menu:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
                selected_level = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_menu = False
                    selected_level = None
                elif event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(levels) - 1, selected_index + 1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if levels:
                        selected_level = levels[selected_index]
                    running_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos
                    item_height = 40
                    start_y = 150
                    for i, lvl in enumerate(levels):
                        text_y = start_y + i * item_height
                        text_rect = pygame.Rect(100, text_y, 400, item_height)
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            selected_level = lvl
                            running_menu = False
                            break

        title_surface = font.render("Selecciona un nivel", True, (255, 255, 255))
        screen.blit(title_surface, (100, 50))

        # Listado de niveles
        item_height = 40
        start_y = 150
        for i, lvl in enumerate(levels):
            color = (200, 200, 200)
            if i == selected_index:
                color = (255, 215, 0)  
            text_surface = font.render(lvl, True, color)
            text_y = start_y + i * item_height
            screen.blit(text_surface, (100, text_y))

        # ostrar vista previa del nivel seleccionado
        if levels:
            current_level_name = levels[selected_index]
            current_maze = previews[current_level_name]

            # clculamos un "tile_size" pequeñoo para el preview
            # buscamos que quepa en un recuadro, por ejemplo 200x200
            max_preview_width = 200
            max_preview_height = 200

            # Evitar división por cero/ si no pones esto, causa problemas 
            if current_maze.cols > 0 and current_maze.rows > 0:
                tile_size_x = max_preview_width // current_maze.cols
                tile_size_y = max_preview_height // current_maze.rows
                preview_tile_size = min(tile_size_x, tile_size_y)
            else:
                preview_tile_size = 10 

            preview_offset_x = 450
            preview_offset_y = 150

            pygame.draw.rect(screen, (50, 50, 50), 
                             (preview_offset_x - 10, preview_offset_y - 10, 
                              max_preview_width + 20, max_preview_height + 20))

            # Llamamos a draw_at con ese tile_size
            current_maze.draw_at(screen, preview_tile_size, preview_offset_x, preview_offset_y)

            # Texto "Preview"
            preview_text = font.render("Preview", True, (255, 255, 255))
            screen.blit(preview_text, (preview_offset_x, preview_offset_y - 40))

        pygame.display.flip()
        clock.tick(60)

    return selected_level


def show_main_menu(screen, clock):
    """
    Argumentos:
        screen (pygame.Surface): Ventana principal de Pygame
        clock (pygame.time.Clock): Reloj de Pygame para regular FPS
    Descripción:
        Función que se encarga de orquestar el menú principal:
        - Obtiene la lista de niveles
        - Llama a run_menu_scene para que el usuario seleccione uno
    Salidas:
        selected_level (str o None): El nivel elegido o None si se sale
    """
    levels = list_levels("data/mazes/")
    if not levels:
        print("No hay niveles disponibles.")
        return None

    selected_level = run_menu_scene(screen, clock, levels)
    return selected_level
