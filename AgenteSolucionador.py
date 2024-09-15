import heapq
from AgenteIA.AgenteBuscador import AgenteBuscador


class AgenteSolucionador(AgenteBuscador):
    def __init__(self):
        super().__init__()
        self.estado_meta = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def buscar(self, estado_inicial):
        return self.tecnica(estado_inicial)
    
    def busqueda_a_star(self, estado_inicial):
        frontera = []
        heapq.heappush(frontera, (0 + self.heuristica(estado_inicial), 0, estado_inicial, []))
        visitados = set()
        
        while frontera:
            self.n_frontera = len(frontera)
            _, costo, estado, camino = heapq.heappop(frontera)
            
            if estado == self.estado_meta:
                return camino
            
            if tuple(estado) in visitados:
                continue

            visitados.add(tuple(estado))
            for siguiente_estado, accion in self.sucesores(estado):
                if tuple(siguiente_estado) not in visitados:
                    nuevo_costo = costo + 1
                    heapq.heappush(frontera, (nuevo_costo + self.heuristica(siguiente_estado), nuevo_costo, siguiente_estado, camino + [accion]))
        return None
    
    def busqueda_codiciosa(self, estado_inicial):
        frontera = []
        heapq.heappush(frontera, (self.heuristica(estado_inicial), estado_inicial, []))
        visitados = set()
        
        while frontera:
            self.n_frontera = len(frontera)
            _, estado, camino = heapq.heappop(frontera)
            
            if estado == self.estado_meta:
                return camino
            
            if tuple(estado) in visitados:
                continue

            visitados.add(tuple(estado))            
            for siguiente_estado, accion in self.sucesores(estado):
                if tuple(siguiente_estado) not in visitados:
                    heapq.heappush(frontera, (self.heuristica(siguiente_estado), siguiente_estado, camino + [accion]))
        
        return None

    def sucesores(self, estado):
        sucesores = []
        blank_index = estado.index(0)
        fila, col = divmod(blank_index, 3)
        
        movimientos = [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]
        for accion, (df, dc) in movimientos:
            nuevo_fila, nuevo_col = fila + df, col + dc
            if 0 <= nuevo_fila < 3 and 0 <= nuevo_col < 3:
                nuevo_index = nuevo_fila * 3 + nuevo_col
                nuevo_estado = estado[:]
                nuevo_estado[blank_index], nuevo_estado[nuevo_index] = nuevo_estado[nuevo_index], nuevo_estado[blank_index]
                sucesores.append((nuevo_estado, accion))
        return sucesores

