# Students

- Responsible of the codes: Andia Telmo
- Responsible of the documentation: Andia Telmo
- Responsible of the unit tests: Leluan Rémi


#DESCRIPTION

This project contains several implementations of player algorithms for PyRat, a simulation game where players compete to collect cheese in a maze. Below, you will find detailed descriptions of the three "Greedy" algorithms we developed.


# Players

*Please write here a few lines on the players you wrote.*
*Precise which choices you made, and why.*
*If you chose to create some functions, which ones and why?*
*What is the complexity of these functions?*
*Did you use defensive programming? if so, where and how?*

<write here>
The Greedy player precomputes a complete path that passes through all pieces of cheese by selecting the closest cheese at each step. Once this path is computed, the player follows it to collect the cheese.

How it works:

Preprocessing:
The path is computed before the game starts using a greedy heuristic.
At each step, the closest piece of cheese is added to the path.
Turn by Turn:
The player moves along the precomputed path, one step at a time.
Advantages:

Simple and efficient in static environments.
Disadvantages:

The player does not adapt if an opponent grabs a targeted piece of cheese.
-GreedyEachCheese
Description:
The GreedyEachCheese player improves upon the Greedy player by recalculating the target only when a piece of cheese is reached. This allows for better adaptation to changes in the environment.

How it works:

Preprocessing:
No complete path is precomputed.
Turn by Turn:
If the current cheese target is reached, the player calculates the next closest cheese.
The player moves one step toward the current target cheese.
Advantages:

More flexible and reactive than the basic Greedy approach.
Disadvantages:

Slightly slower due to on-the-fly calculations.
-GreedyEachTurn
Description:
The GreedyEachTurn player recalculates the closest cheese at every turn. Unlike GreedyEachCheese, this algorithm ensures the player dynamically adapts to changes in the maze or opponent behavior after each movement.

How it works:

Preprocessing:
No precomputation is done.
Turn by Turn:
At each turn, the player calculates the closest piece of cheese and determines the next move accordingly.
Advantages:

Fully reactive to changes, such as when opponents grab cheese.
Optimal for dynamic and competitive scenarios.
Disadvantages:

Increased computational cost due to recalculating paths at every turn.

# Games

*Please write here a few lines on the game scripts you created.*
*What are they made for?*
*Did you change some game parameters? If so, which ones and why?*

<write here>
-Running Matches
To observe how the players perform in a competitive environment, you can simulate matches using PyRat. Below are examples of match configurations for the different greedy algorithms:

-Match: Greedy vs. GreedyEachTurn
Description:
This match pits the basic Greedy algorithm against the dynamic GreedyEachTurn player to compare their efficiency in collecting cheese.

# Unit tests

*Please write here a few lines on the tests you designed.*
*What are they testing?*
*Do you test some error use cases?*
*Are there some missing tests you would have liked to make?*

<write here>

test_traversal:
Ensures the traversal method correctly computes distances and routing tables.
Verifies that all vertices are visited and distances are logically consistent.
Confirms the routing table forms a tree rooted at the start vertex.

Pathfinding Tests

Test compute_greedy_path for all three algorithms to ensure the correct order of cheese collection.
Test find_closest_cheese to verify that the shortest path to the nearest cheese is selected.
Edge Case Tests

No Cheese: The player should stay in its initial position.
One Cheese: The player should directly move to the only available piece of cheese.
Distant Cheese: Ensure the path calculation avoids unnecessary detours.

Error Use Cases
The following scenarios were explicitly tested to handle potential errors:

Invalid Maze Configuration:
Test for disconnected graphs or unreachable cheese.
Opponent Interference:
Simulate scenarios where the opponent collects a cheese before the player reaches it.
Empty Maze:
Ensure the algorithms behave correctly when no maze structure or cheese is defined.

# Utils

*Did you provide anything in the `utils` directory?*
*What are those files?*

<write here>



# Documentation

*Anything to say regarding the documentation?*

<write here>



# Others

*If you had to answer particular questions in the practical session, write your answers here*
*Did you make some interesting analyses?*
*Does your code have particular dependencies we should install ?*
*Anything else to add?*

<write here>