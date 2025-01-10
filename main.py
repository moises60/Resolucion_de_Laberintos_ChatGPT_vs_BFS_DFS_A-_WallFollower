import pygame
import sys
from labyrinth.maze import Maze
from menu.main_menu import show_main_menu
from labyrinth.robot import Robot  
from algorithms.bfs import solve_maze_bfs
from algorithms.dfs import solve_maze_dfs
from algorithms.astar import solve_maze_astar
from algorithms.wall_follower import follow_wall
from algorithms.openai_api_gpt import solve_with_openai_gpt
from algorithms.openai_api_o1 import solve_with_openai_o1



def play_single_level(maze):
    tile_size = 80
    screen_width = maze.cols * tile_size
    screen_height = maze.rows * tile_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Lab con Robot - BFS / DFS / Ruta en pantalla")
    clock = pygame.time.Clock()

    # Posición inicial del robot y "meta"
    start_row, start_col = 1, 1
    goal = (maze.rows - 2, maze.cols - 2)

    # Creamos el robot
    robot = Robot(start_row=start_row, start_col=start_col, color=(255, 0, 0))

    # Variables para la ruta
    path = None      # Almacenará la lista de celdas (row, col)
    path_index = 0   # Índice para el movimiento automático
    show_path = True # Para decidir si dibujar la ruta en pantalla
    moving_automatically = False  # Para distinguir entre moverse automáticamente o manual

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Movimiento manual (solo si no está en auto)
                if not moving_automatically:
                    if event.key == pygame.K_UP:
                        robot.move(maze, -1, 0)
                    elif event.key == pygame.K_DOWN:
                        robot.move(maze, 1, 0)
                    elif event.key == pygame.K_LEFT:
                        robot.move(maze, 0, -1)
                    elif event.key == pygame.K_RIGHT:
                        robot.move(maze, 0, 1)

                # BFS
                if event.key == pygame.K_b:
                    print("Calculando ruta con BFS...")
                    start = (robot.row, robot.col)
                    path = solve_maze_bfs(maze, start, goal)
                    if path is None:
                        print("No se encontró ruta con BFS.")
                        moving_automatically = False
                    else:
                        print(f"Ruta BFS con {len(path)} celdas encontrada.")
                        path_index = 0
                        moving_automatically = True

                # DFS
                if event.key == pygame.K_d:
                    print("Calculando ruta con DFS...")
                    start = (robot.row, robot.col)
                    path = solve_maze_dfs(maze, start, goal)
                    if path is None:
                        print("No se encontró ruta con DFS.")
                        moving_automatically = False
                    else:
                        print(f"Ruta DFS con {len(path)} celdas encontrada.")
                        path_index = 0
                        moving_automatically = True

                # A* con A
                if event.key == pygame.K_a:
                    print("Calculando ruta con A*...")
                    start = (robot.row, robot.col)
                    path = solve_maze_astar(maze, start, goal)
                    if path is None:
                        print("A*: No se encontró ruta.")
                        moving_automatically = False
                    else:
                        print(f"A*: Ruta con {len(path)} celdas encontrada.")
                        path_index = 0
                        moving_automatically = True 
                # W => follow_wall
                if event.key == pygame.K_w:
                    print("Calculando ruta con Wall Follower (derecha)...")
                    start = (robot.row, robot.col)
                    path = follow_wall(maze, start, goal, side="right")
                    if path is None:
                        print("Wall follower: No halló ruta o quedó encerrado.")
                        moving_automatically = False
                    else:
                        print(f"Wall follower: ruta con {len(path)} celdas.")
                        path_index = 0
                        moving_automatically = True
                # OpenAI con O
                if event.key == pygame.K_o:
                    print("Solicitando ruta a OpenAI...")
                    start_pos = (robot.row, robot.col)
                    path = solve_with_openai_gpt(maze, start_pos, goal)
                    #path = solve_with_openai_o1(maze, start_pos, goal)
                    if path is None:
                        print("OpenAI: no se recibió una ruta válida (None o error).")
                        moving_automatically = False
                    else:
                        print(f"OpenAI: ruta con {len(path)} celdas.")
                        path_index = 0
                        moving_automatically = True
                # R => resetear robot
                if event.key == pygame.K_r:
                    print("Reiniciando posición del robot...")
                    robot.row = start_row
                    robot.col = start_col
                    path = None
                    path_index = 0
                    moving_automatically = False

        # Si tenemos una ruta y estamos en modo autoo avanzar paso a paso
        if moving_automatically and path is not None:
            if path_index < len(path):
                # Avanzar 1 celda
                r, c = path[path_index]
                robot.row, robot.col = r, c
                path_index += 1
            else:
                # Ya terminamos la ruta
                moving_automatically = False
                print("Robot llegó al destino.")

            # Pequeño delay para que se vea la animación
            pygame.time.delay(50)

        screen.fill((0, 0, 0))

        # Dibujar el laberinto
        maze.draw(screen, tile_size)

        # Dibujar la ruta en verde (si existe y show_path = True)
        # (Lo hacemos ANTES de dibujar al robot, para que este último quede arriba)
        if show_path and path is not None:
            for (r, c) in path:
                x = c * tile_size
                y = r * tile_size
                pygame.draw.rect(screen, (0, 255, 0), (x, y, tile_size, tile_size), 2)

        # Dibujar el robot
        robot.draw(screen, tile_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def ask_algorithm():
    """
    Muestra un menú en consola para elegir algoritmo o modo de juego
    Devuelve una cadena representando la opción elegida:
      'B' -> BFS
      'D' -> DFS
      'A' -> A*
      'W' -> Wall Follower
      'O' -> OpenAI
      'M' -> Reiniciar
    """
    print("=== Menú de Algoritmos ===")
    print("[B] BFS")
    print("[D] DFS")
    print("[A] A*")
    print("[W] Wall Follower")
    print("[O] OpenAI")
    print("[R] Reiniciar")



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Menú de Laberintos con Preview")
    clock = pygame.time.Clock()

    # Muestra el menú gráfico
    selected_level = show_main_menu(screen, clock)
    if selected_level:
        ask_algorithm()
        maze = Maze()
        maze.load_from_file(f"data/mazes/{selected_level}")
        print(f"Laberinto {selected_level} cargado. Iniciando escena de juego...")
        play_single_level(maze)
    else:
        print("No se ha seleccionado nivel o se cerró el menú.")
    sys.exit()

if __name__ == "__main__":
    main()
