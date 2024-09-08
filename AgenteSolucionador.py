from AgenteIA.AgenteBuscador import AgenteBuscador
import heapq

class AgenteSolucionador:
    def __init__(self):
        AgenteBuscador.__init__(self)
        self.estado_meta = [8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.heuristicas = {
            "manhattan": self.heuristica_manhattan,
            "misplaced": self.heuristica_misplaced,
            "combinada": self.heuristica_combinada
        }
        self.heuristica_actual = None

    def set_heuristica(self, tecnica):
        if tecnica in self.heuristicas:
            self.tecnica = tecnica
            self.heuristica_actual = self.heuristicas[tecnica]
        else:
            raise ValueError(f"Técnica no reconocida: {tecnica}")

    def heuristica_manhattan(self, estado):
        total_distancia = 0
        for i, tile in enumerate(estado):
            if tile != 0:
                objetivo = self.estado_meta.index(tile)
                fila_actual, col_actual = divmod(i, 3)
                fila_objetivo, col_objetivo = divmod(objetivo, 3)
                total_distancia += abs(fila_actual - fila_objetivo) + abs(col_actual - col_objetivo)
        return total_distancia

    def heuristica_misplaced(self, estado):
        return sum(1 for i, tile in enumerate(estado) if tile != 0 and tile != self.estado_meta[i])

    def heuristica_combinada(self, estado):
        return self.heuristica_manhattan(estado) + self.heuristica_misplaced(estado)

    def buscar(self, estado_inicial):
        if self.tecnica == "codicioso":
            return self.busqueda_codiciosa(estado_inicial, self.estado_meta)
        elif self.tecnica == "a*":
            return self.busqueda_a_star(estado_inicial, self.estado_meta)
        else:
            raise ValueError("Técnica no asignada o no reconocida")

    def busqueda_codiciosa(self, estado_inicial):
        frontera = []
        heapq.heappush(frontera, (self.heuristica_actual(estado_inicial), estado_inicial, []))
        visitados = set()
        
        while frontera:
            _, estado, camino = heapq.heappop(frontera)
            
            if estado == self.estado_meta:
                return camino
            
            if tuple(estado) in visitados:
                continue

            visitados.add(tuple(estado))
            for siguiente_estado, accion in self.sucesores(estado):
                if tuple(siguiente_estado) not in visitados:
                    heapq.heappush(frontera, (self.heuristica_actual(siguiente_estado), siguiente_estado, camino + [accion]))
        return None

    def busqueda_a_star(self, estado_inicial):
        frontera = []
        heapq.heappush(frontera, (0 + self.heuristica_actual(estado_inicial), 0, estado_inicial, []))
        visitados = set()
        
        while frontera:
            _, costo, estado, camino = heapq.heappop(frontera)
            
            if estado == self.estado_meta:
                return camino
            
            if tuple(estado) in visitados:
                continue

            visitados.add(tuple(estado))
            for siguiente_estado, accion in self.sucesores(estado):
                if tuple(siguiente_estado) not in visitados:
                    nuevo_costo = costo + 1
                    heapq.heappush(frontera, (nuevo_costo + self.heuristica_actual(siguiente_estado), nuevo_costo, siguiente_estado, camino + [accion]))
        return None

    def sucesores(self, estado):
        sucesores = []
        indices = [i for i, tile in enumerate(estado) if tile == 0]
        for index in indices:
            fila, col = divmod(index, 3)
            for movimiento, (df, dc) in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
                nuevo_fila, nuevo_col = fila + df, col + dc
                if 0 <= nuevo_fila < 3 and 0 <= nuevo_col < 3:
                    nuevo_index = nuevo_fila * 3 + nuevo_col
                    nuevo_estado = list(estado)
                    nuevo_estado[index], nuevo_estado[nuevo_index] = nuevo_estado[nuevo_index], nuevo_estado[index]
                    sucesores.append((nuevo_estado, movimiento))
        return sucesores
