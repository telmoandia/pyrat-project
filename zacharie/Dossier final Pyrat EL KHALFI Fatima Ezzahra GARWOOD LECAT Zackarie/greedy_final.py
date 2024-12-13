from pyrat import Game, Player, Action
from typing import Dict, List
import numpy

# Fonction pour calculer la densité des fromages
def density(maze, cheese):
    densities = {}
    for c in cheese:
        densities[c] = {}
        for other_c in cheese:
            if c != other_c:
                distances, _ = bfs(maze, c)
                densities[c][other_c] = distances[other_c]
    return densities

# Fonction BFS pour les distances
def bfs(maze, source):
    distances = {}
    routing_table = {}
    queue = [(0, source, None)]

    while queue:
        distance, vertex, parent = queue.pop(0)
        if vertex in distances:
            continue
        distances[vertex] = distance
        routing_table[vertex] = parent

        for neighbor in maze.get_neighbors(vertex):
            if neighbor not in distances:
                queue.append((distance + maze.get_weight(vertex, neighbor), neighbor, vertex))

    return distances, routing_table

# Classe pour le joueur glouton
class GreedyPlayer(Player):
    def preprocessing(self, maze, player_locations, cheese, memory):
        """
        Initialisation des données avant le début du jeu.
        """

        try:
            # Calcul des densités des fromages
            memory.densities = density(maze, cheese)
            print(f"Densities initialized: {memory.densities}")
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            raise e

    def turn(self, maze, maze_width, maze_height, name, teams, player_locations, player_scores, player_muds, cheese, possible_actions, memory):
        """
        Décider d'une action à chaque tour.
        """
        print(f"Turn: Player position = {player_locations[name]}, Cheese positions = {cheese}")
        try:
            # Position actuelle du joueur
            player_pos = player_locations[name]

            # Trouver le fromage le plus proche en termes de densité
            best_choice = None
            best_cost = float('inf')
            for c in cheese:
                cost = memory.densities.get(player_pos, {}).get(c, float('inf'))
                if cost < best_cost:
                    best_cost = cost
                    best_choice = c

            if best_choice is None:
                print("No reachable cheese found!")
                return Action.STOP

            print(f"Best cheese selected: {best_choice}")

            # Trouver le chemin vers ce fromage
            distances, routing_table = bfs(maze, player_pos)
            path = reconstruct_path(routing_table, player_pos, best_choice)
            print(f"Path to cheese: {path}")

            # Convertir le chemin en actions
            actions = locations_to_actions(path, maze_width)
            print(f"Actions to take: {actions}")

            # Retourner la première action
            return actions.pop(0)
        except Exception as e:
            print(f"Error in turn: {e}")
            raise e

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
        random_seed=42,  # Semence aléatoire pour la reproductibilité
        maze_width=config["maze_width"],
        maze_height=config["maze_height"],
        cell_percentage=100 - config["mud_percentage"],  # Pourcentage des cellules sans boue
        nb_cheese=config["nb_cheese"],
        trace_length=config["trace_length"]
    )

    # Ajouter le joueur basé sur la densité des fromages
    player = GreedyPlayer()
    game.add_player(player)

    # Lancer le jeu
    stats = game.start()

    # Afficher les résultats
    print(stats)
