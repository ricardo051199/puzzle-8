from AgenteSolucionador import AgenteSolucionador
from Puzzle import Puzzle

if __name__ == "__main__":
    juego = Puzzle()
    juan = AgenteSolucionador()
    juan.set_tecnica("a*")
    juego.insertar(juan)
    juego.run()
