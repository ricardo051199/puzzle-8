import pygame
import random
from AgenteIA.Entorno import Entorno

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = 300
TILE_SIZE = 100
GRID_SIZE = 3

goal_state = [8, 7, 6, 5, 4, 3, 2, 1, 0]

class Puzzle(Entorno):
    def __init__(self):
        Entorno.__init__(self)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("8-Puzzle")
        self.font = pygame.font.Font(None, 100)
        self.grid = self.shuffle_grid(goal_state)

    def shuffle_grid(self, grid):
        new_grid = grid[:]
        random.shuffle(new_grid)
        while not self.is_solvable(new_grid) or self.is_solved(new_grid):
            random.shuffle(new_grid)
        return new_grid

    def is_solvable(self, grid):
        inversions = 0
        grid_without_blank = [tile for tile in grid if tile != 0]
        for i in range(len(grid_without_blank)):
            for j in range(i + 1, len(grid_without_blank)):
                if grid_without_blank[i] > grid_without_blank[j]:
                    inversions += 1
        return inversions % 2 == 0

    def is_solved(self, grid):
        return grid == goal_state

    def get_percepciones(self, agente):
        return self.grid

    def draw_grid(self):
        self.screen.fill(WHITE)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile_value = self.grid[row * GRID_SIZE + col]
                if tile_value != 0:
                    tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.screen, BLACK, tile_rect)
                    text = self.font.render(str(tile_value), True, WHITE)
                    text_rect = text.get_rect(center=tile_rect.center)
                    self.screen.blit(text, text_rect)

    def evolucionar(self):
        self.handle_input()
        self.draw_grid()
        if self.is_solved(self.grid):
            text = self.font.render("¡Ganaste!", True, RED)
            self.screen.blit(text, (50, 120))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            exit()
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.grid = self.move_tile(self.grid, "up")
                elif event.key == pygame.K_DOWN:
                    self.grid = self.move_tile(self.grid, "down")
                elif event.key == pygame.K_LEFT:
                    self.grid = self.move_tile(self.grid, "left")
                elif event.key == pygame.K_RIGHT:
                    self.grid = self.move_tile(self.grid, "right")

    def move_tile(self, grid, direction):
        blank_index = grid.index(0)
        blank_row, blank_col = blank_index // 3, blank_index % 3

        if direction == "up" and blank_row < 2:
            swap_index = blank_index + 3
        elif direction == "down" and blank_row > 0:
            swap_index = blank_index - 3
        elif direction == "left" and blank_col < 2:
            swap_index = blank_index + 1
        elif direction == "right" and blank_col > 0:
            swap_index = blank_index - 1
        else:
            return grid

        new_grid = grid[:]
        new_grid[blank_index], new_grid[swap_index] = new_grid[swap_index], new_grid[blank_index]
        return new_grid
