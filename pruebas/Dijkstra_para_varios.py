from typing import Dict, Tuple, Optional, Any
from heapq import heappush, heappop
from pyrat import Player, Maze, GameState, Action

class Dijkstra(Player):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor de la clase. Inicializa el jugador.
        """
        super().__init__(*args, **kwargs)
        print("Constructor")
        self.chemin = []

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        """
        Método llamado al inicio del juego para precomputar el camino a todos los quesos.
        """
        self.chemin = self.dijkstra_all_cheeses(maze, game_state)
        print("Preprocessing: Camino completo calculado:", self.chemin)

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        """
        Método llamado en cada turno para determinar la acción a realizar.
        """
        if len(self.chemin) > 0:
            action = maze.locations_to_action(game_state.player_locations[self.name], self.chemin[0])
            self.chemin.pop(0)
        else:
            action = Action.STAY
        return action

    def postprocessing(self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
        """
        Método llamado al final del juego para realizar tareas de limpieza o mostrar estadísticas.
        """
        print("Postprocessing")

    def dijkstra_all_cheeses(self, maze: Maze, game_state: GameState) -> list:
        """
        Encuentra el camino para recoger todos los quesos en el orden más eficiente.
        """
        start = game_state.player_locations[self.name]
        cheeses = game_state.cheese[:]
        chemin = []
        current_position = start

        while cheeses:
            # Calcula Dijkstra desde la posición actual
            distances, parents = self.dijkstra_full(maze, current_position)

            # Encuentra el queso más cercano desde la posición actual
            closest_cheese = min(cheeses, key=lambda cheese: distances.get(cheese, float('inf')))

            # Reconstruye el camino hacia ese queso
            path_to_cheese = self.reconstruct_path(closest_cheese, parents)
            chemin.extend(path_to_cheese)

            # Actualiza la posición actual y elimina el queso recogido
            current_position = closest_cheese
            cheeses.remove(closest_cheese)

        return chemin

    def dijkstra_full(self, maze: Maze, start: int) -> Tuple[Dict[int, int], Dict[int, Optional[int]]]:
        """
        Ejecuta Dijkstra desde un vértice de inicio para calcular distancias y rutas a todos los vértices.
        """
        distances = {start: 0}
        parents = {start: None}
        visited = set()
        queue = [(0, start)]  # (distancia, vértice)

        while queue:
            current_distance, current = heappop(queue)
            if current in visited:
                continue
            visited.add(current)

            for neighbor in maze.get_neighbors(current):
                new_distance = current_distance + 1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    parents[neighbor] = current
                    heappush(queue, (new_distance, neighbor))

        return distances, parents

    def reconstruct_path(self, target: int, parents: Dict[int, Optional[int]]) -> list:
        """
        Reconstruye el camino desde el diccionario de padres.
        """
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path