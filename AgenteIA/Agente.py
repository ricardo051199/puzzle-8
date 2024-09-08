# *************************************************************
# * Clase: Agente                                             *
# * Autor: Victor Estevez                                     *
# * Version: v2023.03.29                                      *
# * Descripcion: Implementacion de agente, percibe de su      *
# *              entorno, mapea las percepciones y modifica   *
# *              su entorno para resolucion de problema       *
# *************************************************************


class Agente:

    def __init__(self):
        self.percepciones = None
        self.acciones = []
        self.vive = True

    def programa(self):
        raise Exception("No existe implementacion")
