from typing import List, Tuple, Any
from pyrat import Player, Maze, GameState, Action

class Greedy(Player):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print("Greedy Cheese Collector Initialized")
        self.path_to_all_cheese: List[int] = []  # Precomputed path through all cheeses

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        """
        Precomputes the path through all cheeses using a greedy heuristic.
        """
        print("Starting preprocessing phase")
        start = game_state.player_locations[self.name]
        cheeses = list(game_state.cheese)  # Convert to list for manipulation
        self.path_to_all_cheese = self.compute_greedy_path(maze, start, cheeses)
        print(f"Precomputed path: {self.path_to_all_cheese}")

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        """
        Executes the next step in the precomputed path.
        """
        print(f"Turn {game_state.turn}: Processing next action")

        if self.path_to_all_cheese:
            current_position = game_state.player_locations[self.name]
            next_position = self.path_to_all_cheese.pop(0)

            # Convert the movement to an action
            action = maze.locations_to_action(current_position, next_position)
            print(f"Moving from {current_position} to {next_position} with action {action}")
        else:
            action = Action.STAY  # Default to staying in place if no path remains
            print("No more moves available. Staying in place.")

        return action

    def compute_greedy_path(self, maze: Maze, start: int, cheeses: List[int]) -> List[int]:
        """
        Computes the path through all cheeses using a greedy heuristic.
        """
        current_position = start
        path = []

        while cheeses:
            # Find the closest cheese
            closest_cheese, shortest_path = self.find_closest_cheese(maze, current_position, cheeses)

            # Add the path to the closest cheese to the overall path
            path.extend(shortest_path)

            # Update the current position and remove the cheese from the list
            current_position = closest_cheese
            cheeses.remove(closest_cheese)

        return path

    def find_closest_cheese(self, maze: Maze, current_position: int, cheeses: List[int]) -> Tuple[int, List[int]]:
        """
        Finds the closest cheese from the current position using Dijkstra's algorithm.
        Returns the cheese's location and the path to it.
        """
        distances = {current_position: 0}
        predecessors = {current_position: None}
        visited = set()
        unvisited = set(maze.vertices)

        while unvisited:
            # Get the unvisited vertex with the smallest distance
            current = min(unvisited, key=lambda cell: distances.get(cell, float('inf')))
            unvisited.remove(current)
            visited.add(current)

            if current in cheeses:
                # Stop as soon as we find the closest cheese
                path = []
                while current is not None:
                    path.append(current)
                    current = predecessors[current]
                path.reverse()
                return path[-1], path  # Return the closest cheese and the path to it

            # Explore neighbors of the current vertex
            for neighbor in maze.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_distance = distances[current] + 1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current

        # This point should not be reached if there are cheeses left
        raise ValueError("No path to any cheese found!")
