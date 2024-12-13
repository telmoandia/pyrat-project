#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
PROGRAM INFORMATION:
This algorithm lets you play Pyrat. It allows you to find cheeses in a labyrinth in an intelligent way.
The aim of Pyrat is to pit two competitors against each other, and the winner is the rat that collects the most cheeses.
The strategy of this algorithm can be divided into two points.
First, the rat searches for areas of cheese density. Then, once the number of cheeses is low enough, the rat follows a greedy method. 
It's not possible to follow a greedy method from the start of the game, as the algorithm is too complex.
Moreover, reasoning by density gives a better view of the game than using the greedy method. 
We switch from the density strategy to the greedy strategy as soon as the number of cheeses is low enough.
The strategy() function makes it easy to modify the parameters defining the moment of changeover.
In strategy(), we've chosen as the changeover condition: less than 15 cheeses remaining or the density of cheeses in the maze is less than 15%.
Please note that the density search algorithm presented below is not optimal, as it is too complex.
We didn't rely on the metagraph, which would have made operations less cumbersome.
However, the program has the merit of being more original than the basic greedy, but above all of working better than it.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from logging import getLogRecordFactory
from pyrat import *
from typing import Union, Dict, Callable, Any, Tuple, List
import numpy
import threading

# External imports

# Previously developed functions


#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################


#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def give_score ( graph:          Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                 current_vertex: int,
                 targets:        List[int]
               ):
    """
        Function that associates two scores to each target: a density score and a distance score
        In:
            * graph:             Graph containing the vertices.
            * current_vertex:    Current location of the player in the maze.
            * targets:           List of the targets

        Out:
            * scores_density:     Scores given to the target regarding the density of cheese arround it
            * distance_score:     Scores given to the target regarding its distance from current position
            * routing_table:      Routing table obtained from the current vertex.
    """
    # DISTANCE SCORE
    distance_score, routing_table = dijkstra(current_vertex,graph)
    print (distance_score) # the lower the distance score, the better

    # DENSITY SCORE
    density_score = {v:0 for v in targets}
    for target in targets:
        distance = dijkstra(target, graph)[0]
        for vertex in targets: 
            if target!=vertex: 
                density_score[target]+= distance[vertex] # to define a cheese's density score, we add up all the distances separating it from other cheeses
    print(density_score) # the lower the density score, the better
    
    return density_score, distance_score, routing_table

def graph_to_metagraph ( graph:    Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                         vertices: List[int]
                       ) ->        Tuple[numpy.ndarray, Dict[int, Dict[int, Union[None, int]]]]:
    
    """
        Function to build a complete graph out of locations of interest in a given graph.
        In:
            * graph:    Graph containing the vertices of interest.
            * vertices: Vertices to use in the complete graph.
        Out:
            * complete_graph: Complete graph of the vertices of interest.
            * routing_tables: Dictionary of routing tables obtained by traversals used to build the complete graph.
    """
    
    complete_graph = {}
    routing_tables = {}

    for vertice in vertices:

        # We apply dijkstra to every vertice
        distances_to_explored_vertices, routing_tables[vertice] = dijkstra(vertice, graph)

        #We add all of the other vertices in the complete graph with the key of the vertice we're working on
        for cheese in vertices:
            if cheese != vertice:
                if vertice not in complete_graph.keys():
                    complete_graph[vertice] = {cheese: distances_to_explored_vertices[cheese]}
                else:
                    complete_graph[vertice][cheese] = distances_to_explored_vertices[cheese]

    return complete_graph, routing_tables


def find_closest(density_score, distance_score):
    """
    Function that returns the nearest target beyond the three targets with the best density score
        In:
            * density_score:      Scores given to the target regarding the density of cheese arround it
            * distance_score:     Scores given to the target regarding its distance from current position

        Out:
            * closest_vertex:     The nearest of the three best-density vertices
    """
    # THE THREE BEST CHEESES IN TERMS OF DENSITY
    sorted_density = sorted(density_score.items(), key=lambda item: item[1])
    best = sorted_density[:3] # the three cheeses with the highest density scores are usually next to each other
    
    # FIND THE CLOSEST BEYOND THESE THREE CHEESES
    best_length=distance_score[best[0][0]]
    closest_vertex=best[0][0]
    for vertex in best:
        if distance_score[vertex[0]] < best_length:
            best_length=distance_score[vertex[0]]
            closest_vertex=vertex[0]
    return closest_vertex

def strategy(cheese,maze_width,maze_height) :
    """
    Function that returns "density" if the density of cheeses in the maze is higher than 15% or the number of cheeses is higher than 15.
    It returns "greedy" otherwise.
    An analysis has shown that our density algorithm is not efficient if the rate of cheeses is too low.
    Furthermore, if there is more than 15 cheeses in the maze,  our greedy algorithm is overwhelmed.
            In:
                * cheese:           List of available pieces of cheese in the maze.
                * maze_height:      Height of the maze in number of cells.
                * maze_width:       Width of the maze in number of cells.
            Out:
                * plan:             Game turn strategy
    """
    nb_cheese = len(cheese)
    density_cheese = nb_cheese/(maze_width*maze_height)
    plan = "greedy"
    if density_cheese >= 0.15 or nb_cheese > 15 :
        plan = "density"
        
    return plan

#####################################################################################################################################################
##################################################### EXECUTED ONCE AT THE BEGINNING OF THE GAME ####################################################
#####################################################################################################################################################

def preprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                    maze_width:       int,
                    maze_height:      int,
                    name:             str,
                    teams:            Dict[str, List[str]],
                    player_locations: Dict[str, int],
                    cheese:           List[int],
                    possible_actions: List[str],
                    memory:           threading.local
                  ) ->                None:

    """
        This function is called once at the beginning of the game.
        It is typically given more time than the turn function, to perform complex computations.
        Store the results of these computations in the provided memory to reuse them later during turns.
        To do so, you can crete entries in the memory dictionary as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """
  

#####################################################################################################################################################
######################################################### EXECUTED AT EACH TURN OF THE GAME #########################################################
#####################################################################################################################################################

def turn ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
           maze_width:       int,
           maze_height:      int,
           name:             str,
           teams:            Dict[str, List[str]],
           player_locations: Dict[str, int],
           player_scores:    Dict[str, float],
           player_muds:      Dict[str, Dict[str, Union[None, int]]],
           cheese:           List[int],
           possible_actions: List[str],
           memory:           threading.local
         ) ->                str:

    """
        This function is called at every turn of the game and should return an action within the set of possible actions.
        You can access the memory you stored during the preprocessing function by doing memory.my_key.
        You can also update the existing memory with new information, or create new entries as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * action: One of the possible actions, as given in possible_actions.
    """
    strat = strategy(cheese,maze_width,maze_height) 
    if strat == "density" :
        density_score, distance_score, routing_table = give_score (maze, player_locations[name], cheese )
        closest_cheese = find_closest(density_score,distance_score)
        next_location = find_route (routing_table, player_locations[name], closest_cheese)[1]
        action=locations_to_action(player_locations[name],next_location, maze_width)
    else: # otherwise strat == "greedy"
        scores, routing_table = give_score_2 (maze, player_locations[name], cheese )
        closest_cheese = find_closest_2(scores)
        next_location = find_route (routing_table, player_locations[name], closest_cheese)[1]
        action=locations_to_action(player_locations[name],next_location, maze_width)
        
    return action

#####################################################################################################################################################
######################################################## EXECUTED ONCE AT THE END OF THE GAME #######################################################
#####################################################################################################################################################

def postprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                     maze_width:       int,
                     maze_height:      int,
                     name:             str,
                     teams:            Dict[str, List[str]],
                     player_locations: Dict[str, int],
                     player_scores:    Dict[str, float],
                     player_muds:      Dict[str, Dict[str, Union[None, int]]],
                     cheese:           List[int],
                     possible_actions: List[str],
                     memory:           threading.local,
                     stats:            Dict[str, Any],
                   ) ->                None:

    """
        This function is called once at the end of the game.
        It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """

    pass

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Map the functions to the character
    players = [{"name": "MIX", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing}]

    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 40.0,
              "nb_cheese": 21,
              "trace_length": 1000}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################