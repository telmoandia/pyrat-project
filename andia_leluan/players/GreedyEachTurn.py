from pyrat import Player, Maze, GameState, Action
from typing import List, Tuple, Any, Optional


class GreedyEachTurn(Player):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print("GreedyEachTurn Player Initialized")

    def preprocessing(self, maze: Maze, game_state: GameState) -> None:
        """
        Precomputations before the game starts. Not required for GreedyEachTurn.
        """
        print("Starting preprocessing phase")
        pass

    def turn(self, maze: Maze, game_state: GameState) -> Action:
        """
        Run the greedy algorithm at each turn to decide the next action.
        """
        print(f"Turn {game_state.turn}: Processing next action")

        current_position = game_state.player_locations[self.name]
        remaining_cheeses = set(game_state.cheese)

        if not remaining_cheeses:
            print("No more cheese to collect. Staying in place.")
            return Action.STAY

        # Find the closest piece of cheese
        closest_cheese = self.find_closest_cheese(maze, current_position, remaining_cheeses)
        print(f"Closest cheese to {current_position} is at {closest_cheese}")

        # Determine the next action to move toward the closest cheese
        next_action = self.get_next_action_toward_cheese(maze, current_position, closest_cheese)
        if next_action:
            print(f"Moving towards {closest_cheese} with action {next_action}")
            return next_action
        else:
            print("No valid action found. Staying in place.")
            return Action.STAY

    def find_closest_cheese(self, maze: Maze, current_position: int, remaining_cheeses: set) -> Optional[int]:
        """
        Finds the closest cheese using Dijkstra's algorithm.
        """
        closest_cheese = None
        min_distance = float('inf')

        for cheese in remaining_cheeses:
            _, distance = self.find_shortest_path(maze, current_position, cheese)
            if distance < min_distance:
                min_distance = distance
                closest_cheese = cheese

        return closest_cheese

    def get_next_action_toward_cheese(self, maze: Maze, current_position: int, target_position: int) -> Optional[Action]:
        """
        Determines the next action to take to move toward the target cheese.
        """
        path, _ = self.find_shortest_path(maze, current_position, target_position)
        if len(path) > 1:
            next_position = path[1]
            return maze.locations_to_action(current_position, next_position)
        return None

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

            if current == end:
                break  # Stop if we reach the destination

            for neighbor in maze.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_distance = distances[current] + 1  # Distance is always 1 per step
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
