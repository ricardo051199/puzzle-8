import pandas as pd
from Puzzle import Puzzle
from AgenteSolucionador import AgenteSolucionador

algoritmos_busqueda = ["codicioso", "a_estrella"]
heuristicas = ["manhattan", "misplaced", "euclidiana"]

def ejecutar_experimentos(num_experimentos):
    resultados = []
    
    for algoritmo in algoritmos_busqueda:
        for heuristica in heuristicas:
            for i in range(num_experimentos):
                puzzle = Puzzle()
                agente = AgenteSolucionador()
                resultado = puzzle.jugar_y_registrar(agente, algoritmo, heuristica)
                resultados.append(resultado)
                
                print(f"Experimento {i+1}/{num_experimentos} completado con {algoritmo} y {heuristica}.")
    
    return resultados

if __name__ == "__main__":
    num_experimentos = 167  # Para cada combinacion (1002 Registros con 6 combinaciones en total)
    resultados = ejecutar_experimentos(num_experimentos)
    
    df = pd.DataFrame(resultados)
    df.to_csv("game1000.csv", index=False)
    print("Experimentos completados y resultados guardados en game1000.csv")
