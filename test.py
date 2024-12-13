from pyrat import Game, Player, Action, GameState
from typing import Dict, List
import numpy




# Fonction BFS pour les distances
# Función BFS para las distancias
# Función BFS para las distancias
def bfs(maze, source):
    distances = {}
    routing_table = {}
    queue = [(0, source, None)]

    while queue:
        distance, vertex, parent = queue.pop(0)

        # Verifica si el vértice ya ha sido visitado
        if vertex in distances:
            continue
        distances[vertex] = distance
        routing_table[vertex] = parent

        # Verifica si el vértice tiene vecinos válidos antes de acceder
        neighbors = maze.get_neighbors(vertex)
        if neighbors is None:  # Si no tiene vecinos
            print(f"Warning: Vertex {vertex} has no neighbors.")
            continue

        # Agrega los vecinos al queue
        for neighbor in neighbors:
            if neighbor not in distances:
                queue.append((distance + maze.get_weight(vertex, neighbor), neighbor, vertex))

    print(f"BFS distances from {source}: {distances}")  # Depuración de las distancias calculadas
    return distances, routing_table

# Clase para el jugador glouton
class DensityPlayer(Player):
    def __init__(self):
        super().__init__()
        self.densities = {}  # Para almacenar densidades calculadas.

    def preprocessing(self, maze, game_state: GameState):
        """
        Inicializa los datos antes del inicio del juego.
        """
        try:
            # Calcular densidades de los quesos
            self.densities = density(maze, game_state.cheese)
            print(f"Densities: {self.densities}")  # Imprimir densidades calculadas
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            raise e

    def turn(self, maze, game_state: GameState):
        """
        Decide una acción en cada turno.
        """
        try:
            # Acceso correcto a la posición del jugador
            player_pos = game_state.player_locations['DensityPlayer']

            # Obtener las posiciones de los quesos desde game_state
            cheese_positions = game_state.cheese

            print(f"Player position: {player_pos}")
            print(f"Cheese positions: {cheese_positions}")

            # Encontrar el queso más cercano
            best_choice = None
            best_cost = float('inf')
            
            for c in cheese_positions:  # Usamos cheese_positions en lugar de 'cheese'
                print(f"Calculating cost for cheese {c}")

                # Obtener el costo para llegar al queso desde la posición actual
                cost = self.densities.get(player_pos, {}).get(c, float('inf'))

                # Depuración de valores
                print(f"Cost to cheese {c}: {cost}, Best cost so far: {best_cost}")

                if cost < best_cost:
                    best_cost = cost
                    best_choice = c
                    print(f"El mejor queso es {best_choice} con un costo de {best_cost}")  # Depuración adicional

            if best_choice is None:
                print("No reachable cheese found!")
                return Action.NOTHING

            print(f"Best cheese selected: {best_choice}")

            # Encontrar el camino hacia el queso
            distances, routing_table = bfs(maze, player_pos)
            path = reconstruct_path(routing_table, player_pos, best_choice)

            # Convertir el camino en acciones
            maze_width = maze.width  # Acceso al ancho del laberinto
            actions = locations_to_actions(path, maze_width)

            # Devolver la primera acción
            return actions.pop(0)

        except Exception as e:
            print(f"Error in turn: {e}")
            raise e




# Función para calcular la densidad de los quesos
def density(maze, cheese):
    densities = {}
    for c in cheese:
        densities[c] = {}
        for other_c in cheese:
            if c != other_c:
                distances, _ = bfs(maze, c)
                densities[c][other_c] = distances.get(other_c, float('inf'))
                print(f"Densities for cheese {c} to {other_c}: {densities[c][other_c]}")  # Debugging line
    return densities


# Convertir une route en une liste d'actions
def locations_to_actions(route, maze_width):
    actions = []
    for i in range(len(route) - 1):
        x1, y1 = route[i] % maze_width, route[i] // maze_width
        x2, y2 = route[i + 1] % maze_width, route[i + 1] // maze_width
        if x2 == x1 + 1:
            actions.append(Action.EAST)
        elif x2 == x1 - 1:
            actions.append(Action.WEST)
        elif y2 == y1 + 1:
            actions.append(Action.SOUTH)
        elif y2 == y1 - 1:
            actions.append(Action.NORTH)
    return actions


# Reconstituer le chemin
def reconstruct_path(routing_table, source, target):
    path = [target]
    while target != source:
        target = routing_table[target]
        path.append(target)
    return path[::-1]


# Configuration du jeu
if __name__ == '__main__':
    config = {
        "maze_width": 31,
        "maze_height": 29,
        "mud_percentage": 10.0,
        "nb_cheese": 41,
        "trace_length": 1000,
    }

    # Création et lancement du jeu
    game = Game(
        random_seed=42,
        maze_width=config["maze_width"],
        maze_height=config["maze_height"],
        cell_percentage=100 - config["mud_percentage"],
        nb_cheese=config["nb_cheese"],
        trace_length=config["trace_length"],
    )

    # Ajouter un joueur basé sur la densité des fromages
    player = DensityPlayer()
    game.add_player(player)

    # Lancer le jeu
    stats = game.start()

    # Afficher les résultats
    print(stats)
