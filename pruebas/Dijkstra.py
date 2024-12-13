from typing import Dict, Tuple, Optional, Any
from numbers import Integral
from pyrat import Player, Maze, GameState, Action

class Dijkstra(Player):
    """
    Player implementation using Dijkstra's algorithm to calculate the shortest path to the cheese.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor for the Dijkstra-based player.
        Initializes the player's attributes and ensures parent class initialization.
        """
        super().__init__(*args, **kwargs)
        print("Dijkstra Player Initialized")
        self.path_to_cheese = []  # Stores the planned path to the cheese

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        """
        Precomputes the shortest path to the cheese using Dijkstra's algorithm.
        """
        print("Starting preprocessing phase")
        self.path_to_cheese = self.compute_dijkstra_path(maze, game_state)

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        """
        Determines the action to take on the current turn.
        Executes the next step in the precomputed path if available.
        """
        print(f"Turn {game_state.turn}: Processing next action")

        if self.path_to_cheese:
            # Convert the next position in the path to an action
            next_position = self.path_to_cheese.pop(0)
            action = maze.locations_to_action(game_state.player_locations[self.name], next_position)
        else:
            action = Action.STAY  # Default to staying in place if no path is available
        
        return action

    def postprocessing(self, maze: Maze, game_state: GameState, stats: Dict[str, Any]) -> None:
        """
        Cleans up or logs information after the game ends.
        """
        print("Game finished. Postprocessing phase complete.")

    def compute_dijkstra_path(self, maze: Maze, game_state: GameState) -> list:
        """
        Implements Dijkstra's algorithm to find the shortest path to the cheese.
        Returns the calculated path as a list of maze locations.
        """
        start = game_state.player_locations[self.name]  # Starting position of the player
        goal = game_state.cheese[0]  # Location of the cheese

        distances = {start: 0}  # Track the minimum distance to each cell
        predecessors = {start: None}  # Track the parent of each cell in the path
        visited = set()  # Cells that have been fully processed
        unvisited = set(maze.vertices)  # Cells yet to be processed

        while unvisited:
            # Select the unvisited cell with the smallest distance
            current = min(unvisited, key=lambda cell: distances.get(cell, float('inf')))
            unvisited.remove(current)
            visited.add(current)

            # Update distances for neighbors
            for neighbor in maze.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_distance = distances[current] + 1  # Assume uniform weight of 1 for all edges
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current

        # Reconstruct the path from the goal to the start
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()  # Reverse the path to go from start to goal

        return path
