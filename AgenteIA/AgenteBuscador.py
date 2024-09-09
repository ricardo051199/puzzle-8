# **********************************************************
# * Clase: Agente buscador                                 *
# * Autor: Victor Estevez                                  *
# * Version: v2023.03.29                                   *
# * Descripcion: Implementacion de algoritmos de busqueda  *
# *              sin informacion y con informacion         *
# **********************************************************

from AgenteIA.Agente import Agente
from copy import deepcopy
import time
import math

class AgenteBuscador(Agente):
    def __init__(self):
        Agente.__init__(self)
        self.estado_inicial = None
        self.estado_meta = None
        self.funcion_sucesor = []
        self.tecnica = None
        self.heuristica = None
        self.n_frontera = 0

    def set_tecnica(self, t):
        if t == "codicioso":
            self.tecnica = self.busqueda_codiciosa
        elif t == "a_estrella":
            self.tecnica = self.busqueda_a_star

    def set_heuristica(self, h):
        if h == "manhattan":
            self.heuristica = self.heuristica_manhattan
        elif h == "misplaced":
            self.heuristica = self.heuristica_misplaced
        elif h == "euclidiana":
            self.heuristica = self.heuristica_euclidiana

    def add_funcion(self, f):
        self.funcion_sucesor.append(f)

    def test_objetivo(self, e):
        return e == self.estado_meta

    def generar_hijos(self, e):
        hijos = []
        for fun in self.funcion_sucesor:
            h = fun(e)
            hijos.append(h)
        return hijos

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
    
    def heuristica_euclidiana(self, estado):
        total_distancia = 0
        for i, tile in enumerate(estado):
            if tile != 0:
                objetivo = self.estado_meta.index(tile)
                fila_actual, col_actual = divmod(i, 3)
                fila_objetivo, col_objetivo = divmod(objetivo, 3)
                distancia = math.sqrt((fila_actual - fila_objetivo) ** 2 + (col_actual - col_objetivo) ** 2)
                total_distancia += distancia
        return total_distancia
    
    def busqueda_codiciosa(self):
        pass

    def busqueda_a_star(self):
        pass
    
    def programa(self):
        frontera = [[self.estado_inicial]]
        visitados = []
        while frontera:
            if self.tecnica == "profundidad":
                camino = frontera.pop()
            else:
                camino = frontera.pop(0)
            nodo = camino[-1]
            visitados.append(nodo)
            if self.test_objetivo(nodo):
                self.acciones = camino
                break
            else:
                for hijo in self.generar_hijos(nodo):
                    if hijo not in visitados:
                        aux = deepcopy(camino)
                        aux.append(hijo)
                        frontera.append(aux)
                if self.tecnica == "codicioso":
                    frontera.sort(key=lambda tup: self.busqueda_codiciosa(tup))
                elif self.tecnica == "a_estrella":
                    frontera.sort(key=lambda tup: self.busqueda_a_star(tup))
