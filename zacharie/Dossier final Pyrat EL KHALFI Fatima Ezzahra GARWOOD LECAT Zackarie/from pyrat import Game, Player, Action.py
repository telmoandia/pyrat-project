from pyrat import Game, Player, Action

# Classe pour le joueur glouton
class GreedyPlayer(Player):
    def preprocessing(
        self,
        maze,
        maze_width,
        maze_height,
        name,
        teams,
        player_locations,
        cheese,
        possible_actions,
        memory
    ):
        """
        Initialisation des données avant le début du jeu.
        """
        print(f"Preprocessing: Maze size = {maze_width}x{maze_height}, Player = {name}")
        print(f"Cheese positions received: {cheese}")
        memory.densities = {c: {} for c in cheese}  # Exemple simple d'initialisation
        print("Memory initialized.")

    def turn(
        self,
        maze,
        maze_width,
        maze_height,
        name,
        teams,
        player_locations,
        player_scores,
        player_muds,
        cheese,
        possible_actions,
        memory
    ):
        """
        Décide quelle action prendre à chaque tour.
        """
        print(f"Turn: Player position = {player_locations[name]}, Cheese positions = {cheese}")
        print(f"Possible actions: {possible_actions}")

        if cheese:
            return Action.NORTH  # Exemple simple pour tester
        return Action.STOP

# Configuration du jeu
if __name__ == "__main__":
    config = {
        "maze_width": 31,
        "maze_height": 29,
        "mud_percentage": 10.0,
        "nb_cheese": 41,
        "trace_length": 1000,
    }

    # Création et configuration du jeu
    game = Game(
        random_seed=42,
        maze_width=config["maze_width"],
        maze_height=config["maze_height"],
        cell_percentage=100 - config["mud_percentage"],
        nb_cheese=config["nb_cheese"],
        trace_length=config["trace_length"],
    )

    # Ajouter un joueur
    player = GreedyPlayer()
    game.add_player(player)

    # Lancer le jeu
    stats = game.start()

    # Afficher les statistiques
    print(stats)
