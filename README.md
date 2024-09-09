
# 8-Puzzle Game & Experiments

Este repositorio contiene un juego del rompecabezas de 8 fichas, implementado en Python usando Pygame y agentes inteligentes. Además, incluye un módulo de experimentación que realiza simulaciones automáticas con diferentes algoritmos de búsqueda y heurísticas.

## Requisitos

Antes de ejecutar el juego o los experimentos, asegúrate de tener instaladas las siguientes dependencias:

- Pygame
- Pandas

### Instalación de dependencias

Puedes instalar las dependencias ejecutando el siguiente comando:

```bash
pip install pygame pandas
```

## Cómo ejecutar el juego

### 1. Ejecutar el juego de forma manual

Para jugar manualmente, ejecuta el archivo `main.py`:

```bash
python main.py
```

#### Controles del juego

- **Teclas de dirección (↑, ↓, ←, →)**: Mueven la ficha vacía (espacio en blanco) en la dirección correspondiente.
- **Tecla `ESPACIO`**: Resuelve automáticamente el rompecabezas utilizando el algoritmo A* con la heurística Manhattan.
  
#### Objetivo del juego

El objetivo del juego es ordenar las fichas numeradas del 1 al 8, con la ficha vacía (0) al final, de la siguiente manera:

```
8  7  6
5  4  3
2  1  0
```

Cuando logres ordenar las fichas en el estado objetivo, el juego mostrará un mensaje de "¡Ganaste!" en pantalla y se cerrará automáticamente.

### 2. Ejecutar el experimento con 1000 simulaciones

Para ejecutar los experimentos y registrar los resultados, ejecuta el archivo `experimento.py`:

```bash
python experimento.py
```

Este archivo realizará 1000 simulaciones del juego con diferentes combinaciones de algoritmos y heurísticas, y registrará los siguientes datos en un archivo `game1000.csv`:

- **Estado inicial**: La disposición inicial de las fichas.
- **Movimientos**: La secuencia de movimientos realizados para resolver el puzzle.
- **Algoritmo de búsqueda**: Algoritmo utilizado para resolver el puzzle (ej. `a_estrella` o `codicioso`).
- **Heurística**: Heurística utilizada (ej. `manhattan`, `misplaced`, `euclidiana`).
- **Tiempo de resolución**: Tiempo total necesario para resolver el puzzle.
- **Tamaño de la frontera**: Número de nodos explorados durante la búsqueda.
- **Ganó**: Indica si el puzzle fue resuelto o no.

### 3. Resultados de los experimentos

Al finalizar las simulaciones, los resultados serán guardados en un archivo `game1000.csv` en el mismo directorio del proyecto. Este archivo puede abrirse con programas como Excel, Google Sheets o cualquier otro lector de CSV.

---

