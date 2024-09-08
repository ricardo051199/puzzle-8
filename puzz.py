import pygame
import random

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configuración de la pantalla
SCREEN_SIZE = 300
TILE_SIZE = 100
GRID_SIZE = 3

# Generar la grilla objetivo
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Inicializar pygame
pygame.init()

# Crear la ventana
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("8-Puzzle")

# Fuente para los números
font = pygame.font.Font(None, 100)

# Función para dibujar la grilla
def draw_grid(grid):
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_value = grid[row * GRID_SIZE + col]
            if tile_value != 0:  # No dibujar la casilla vacía
                tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLACK, tile_rect)
                text = font.render(str(tile_value), True, WHITE)
                text_rect = text.get_rect(center=tile_rect.center)
                screen.blit(text, text_rect)

# Función para verificar si el juego está en estado objetivo
def is_solved(grid):
    return grid == goal_state

# Mover una ficha en la dirección especificada
def move_tile(grid, direction):
    blank_index = grid.index(0)
    blank_row, blank_col = blank_index // GRID_SIZE, blank_index % GRID_SIZE

    if direction == "up" and blank_row < GRID_SIZE - 1:
        swap_index = blank_index + GRID_SIZE
    elif direction == "down" and blank_row > 0:
        swap_index = blank_index - GRID_SIZE
    elif direction == "left" and blank_col < GRID_SIZE - 1:
        swap_index = blank_index + 1
    elif direction == "right" and blank_col > 0:
        swap_index = blank_index - 1
    else:
        return grid  # Movimiento no permitido, no hacer nada

    # Intercambiar la casilla vacía con la ficha adyacente
    new_grid = grid[:]
    new_grid[blank_index], new_grid[swap_index] = new_grid[swap_index], new_grid[blank_index]
    return new_grid

# Barajar la grilla
def shuffle_grid(grid):
    new_grid = grid[:]
    random.shuffle(new_grid)
    while not is_solvable(new_grid) or is_solved(new_grid):
        random.shuffle(new_grid)
    return new_grid

# Función para verificar si la grilla es resolvible
def is_solvable(grid):
    inversions = 0
    grid_without_blank = [tile for tile in grid if tile != 0]
    for i in range(len(grid_without_blank)):
        for j in range(i + 1, len(grid_without_blank)):
            if grid_without_blank[i] > grid_without_blank[j]:
                inversions += 1
    return inversions % 2 == 0

# Estado inicial
grid = shuffle_grid(goal_state)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                grid = move_tile(grid, "up")
            elif event.key == pygame.K_DOWN:
                grid = move_tile(grid, "down")
            elif event.key == pygame.K_LEFT:
                grid = move_tile(grid, "left")
            elif event.key == pygame.K_RIGHT:
                grid = move_tile(grid, "right")

    draw_grid(grid)

    # Comprobar si el jugador ha ganado
    if is_solved(grid):
        text = font.render("¡Ganaste!", True, RED)
        screen.blit(text, (50, 120))

    pygame.display.flip()

pygame.quit()
