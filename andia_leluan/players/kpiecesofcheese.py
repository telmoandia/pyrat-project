from typing import List, Tuple, Any, Dict
from pyrat import Player, Maze, GameState, Action
from itertools import permutations
from functools import lru_cache


class GreedyBestDPieces(Player):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print("Optimized Greedy Best d Pieces Initialized")
        self.path_to_cheese: List[int] = []  # Precomputed path to the cheese
        self.depth = 3  # Set depth d for the heuristic
        self.memoized_distances: Dict[Tuple[int, int], Tuple[List[int], int]] = {}  # Cache distances

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        """
        Precomputes the optimal path using the Best d Pieces heuristic.
        """
        print("Starting preprocessing phase")
        self.depth = min(self.depth, len(game_state.cheese))  # Adjust depth to the number of cheeses
        start = game_state.player_locations[self.name]
        cheeses = list(game_state.cheese)
        self.memoized_distances = {}  # Clear cache
        self.path_to_cheese = self.compute_best_d_path(maze, start, cheeses)
        print(f"Precomputed path: {self.path_to_cheese}")

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        """
        Determines the action to take on the current turn.
        """
        print(f"Turn {game_state.turn}: Processing next action")
        current_position = game_state.player_locations[self.name]
        cheeses = list(game_state.cheese)

        if not cheeses:
            print("No cheeses left. Staying in place.")
            return Action.STAY

        # Recompute path if necessary
        if not self.path_to_cheese or self.path_to_cheese[0] not in cheeses:
            self.path_to_cheese = self.compute_best_d_path(maze, current_position, cheeses)

        # Take the next step along the path
        if self.path_to_cheese:
            next_position = self.path_to_cheese.pop(0)
            action = maze.locations_to_action(current_position, next_position)
            print(f"Moving to {next_position} with action {action}")
            return action
        else:
            print("No valid path found. Staying in place.")
            return Action.STAY

    def compute_best_d_path(self, maze: Maze, start: int, cheeses: List[int]) -> List[int]:
        """
        Computes the optimal path using the Best d Pieces heuristic.
        """
        best_path = []
        best_distance = float('inf')

        # Generate all permutations of cheeses up to depth d
        for sequence in permutations(cheeses, self.depth):
            current_position = start
            current_path = []
            total_distance = 0

            for cheese in sequence:
                path, distance = self.get_distance(maze, current_position, cheese)
                current_path.extend(path[1:])  # Add path except the starting position
                total_distance += distance
                current_position = cheese

            if total_distance < best_distance:
                best_distance = total_distance
                best_path = current_path

        return best_path

    def get_distance(self, maze: Maze, start: int, end: int) -> Tuple[List[int], int]:
        """
        Fetches the distance and path between two points, using a cache to speed up computations.
        """
        if (start, end) not in self.memoized_distances:
            self.memoized_distances[(start, end)] = self.find_shortest_path(maze, start, end)
        return self.memoized_distances[(start, end)]

    def find_shortest_path(self, maze: Maze, start: int, end: int) -> Tuple[List[int], int]:
        """
        Finds the shortest path between two points using Dijkstra's algorithm.
        """
        distances = {start: 0}
        predecessors = {start: None}
        visited = set()
        unvisited = set(maze.vertices)

        while unvisited:
            current = min(unvisited, key=lambda cell: distances.get(cell, float('inf')))
            unvisited.remove(current)
            visited.add(current)

            if current == end:
                break

            for neighbor in maze.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_distance = distances[current] + 1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current

        # Reconstruct the path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return path, distances[end]
