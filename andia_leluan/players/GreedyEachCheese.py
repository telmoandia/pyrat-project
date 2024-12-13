from pyrat import Player, Maze, GameState, Action
from typing import List, Tuple, Any, Set


class GreedyEachCheese(Player):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print("GreedyEachCheese Player Initialized")

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        """
        No precomputations are required for this greedy strategy.
        """
        print("Starting preprocessing phase")
        pass

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        """
        Determines the action to take on the current turn.
        Finds the closest piece of cheese and moves toward it.
        """
        print(f"Turn {game_state.turn}: Processing next action")

        current_position = game_state.player_locations[self.name]
        remaining_cheeses = set(game_state.cheese)

        if not remaining_cheeses:
            print("No more cheese to collect. Staying in place.")
            return Action.STAY

        # Find the closest cheese
        next_cheese = self.find_closest_cheese(maze, current_position, remaining_cheeses)
        print(f"Closest cheese to {current_position} is at {next_cheese}")

        # Determine the action to move toward the closest cheese
        path_to_cheese, _ = self.find_shortest_path(maze, current_position, next_cheese)
        if len(path_to_cheese) > 1:
            next_position = path_to_cheese[1]  # First step toward the cheese
            action = maze.locations_to_action(current_position, next_position)
            print(f"Moving from {current_position} to {next_position} with action {action}")
            return action
        else:
            print("No valid path to the cheese. Staying in place.")
            return Action.STAY

    def find_closest_cheese(self, maze: Maze, current_position: int, remaining_cheeses: Set[int]) -> int:
        """
        Finds the closest cheese from the current position using the shortest path.
        """
        closest_cheese = None
        min_distance = float('inf')

        for cheese in remaining_cheeses:
            _, distance = self.find_shortest_path(maze, current_position, cheese)
            if distance < min_distance:
                min_distance = distance
                closest_cheese = cheese

        return closest_cheese

    def find_shortest_path(self, maze: Maze, start: int, end: int) -> Tuple[List[int], int]:
        """
        Finds the shortest path between two points (start and end) using Dijkstra's algorithm.
        """
        distances = {start: 0}
        predecessors = {start: None}
        visited = set()
        unvisited = set(maze.vertices)

        while unvisited:
            current = min(unvisited, key=lambda cell: distances.get(cell, float('inf')))
            unvisited.remove(current)

            if current == end:
                break  # Stop if the end point is reached

            for neighbor in maze.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_distance = distances[current] + 1  # Each step has a distance of 1
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

        return path, distances.get(end, float('inf'))
