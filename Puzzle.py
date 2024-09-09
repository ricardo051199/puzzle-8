import time
import pygame
import random
from AgenteIA.Entorno import Entorno
from AgenteSolucionador import AgenteSolucionador

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = 300
TILE_SIZE = 100
GRID_SIZE = 3

goal_state = [8, 7, 6, 5, 4, 3, 2, 1, 0]

class Puzzle(Entorno):
    def __init__(self, grid=None):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("8-Puzzle")
        self.font = pygame.font.Font(None, 100)
        self.grid = self.shuffle_grid(goal_state)
        if grid is None:
            self.grid = self.shuffle_grid(goal_state)
            self.auto = False
        else:
            self.grid = grid
            self.auto = True
        
        self.estado_inicial = self.grid

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

    def ejecutar(self, agente):
        self.handle_input(agente)
        self.draw_grid()
        if self.is_solved(self.grid):
            text = self.font.render("¡Ganaste!", True, RED)
            self.screen.blit(text, (50, 120))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            exit()
        pygame.display.flip()

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

    def handle_input(self, agente):
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
                elif event.key == pygame.K_SPACE or self.auto == True:
                    mejor_camino = agente.buscar(self.grid)
                    if mejor_camino:
                        for accion in mejor_camino:
                            self.grid = self.move_tile(self.grid, accion)
                            self.draw_grid()
                            pygame.display.flip()
                            pygame.time.wait(5)

    def move_tile(self, grid, direction):
        blank_index = grid.index(0)
        blank_row, blank_col = blank_index // 3, blank_index % 3

        if direction == "up" and blank_row > 0:
            swap_index = blank_index - 3
        elif direction == "down" and blank_row < 2:
            swap_index = blank_index + 3
        elif direction == "left" and blank_col > 0:
            swap_index = blank_index - 1
        elif direction == "right" and blank_col < 2:
            swap_index = blank_index + 1
        else:
            return grid

        new_grid = grid[:]
        new_grid[blank_index], new_grid[swap_index] = new_grid[swap_index], new_grid[blank_index]
        return new_grid
    
    def obtener_informacion_buscador(self, agente):
        estado_inicial = list(self.grid)
        movimientos = []
        algoritmo_busqueda = agente.tecnica
        heuristica = agente.heuristica
        tiempo_resolucion = 0
        n_frontera = 0
        gano = False
        start_time = time.time()
        mejor_camino = agente.buscar(self.grid)
        tiempo_resolucion = time.time() - start_time
        
        if mejor_camino:
            movimientos = mejor_camino
            gano = True
            n_frontera = agente.n_frontera
        
        return {
            'estado_inicial': estado_inicial,
            'movimientos': movimientos,
            'algoritmo_busqueda': algoritmo_busqueda,
            'heuristica': heuristica,
            'tiempo_resolucion': tiempo_resolucion,
            'tamaño_frontera': n_frontera,
            'gano': gano
        }
    
    def jugar_y_registrar(self, agente, tecnica, heuristica):
        # Configurar el agente
        agente.set_tecnica(tecnica)
        agente.set_heuristica(heuristica)
        
        # Guardar el estado inicial
        estado_inicial = self.grid
        
        # Iniciar el temporizador
        start_time = time.time()
        
        # Ejecutar el agente para encontrar el mejor camino
        mejor_camino = agente.buscar(self.grid)

        if mejor_camino:
            for accion in mejor_camino:
                self.grid = self.move_tile(self.grid, accion)
                self.draw_grid()

        end_time = time.time()
        
        tiempo_resolucion = end_time - start_time
        
        if self.grid == [8,7,6,5,4,3,2,1,0]:
            gano = True


        return {
            "estado_inicial": estado_inicial,
            "movimientos": mejor_camino,
            "algoritmo_busqueda": tecnica,
            "heuristica": heuristica,
            "tiempo_resolucion": tiempo_resolucion,
            "tamaño_frontera": agente.n_frontera,
            "gano": gano
        }
