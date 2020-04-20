# Battleships
Battleships python game

This game was made using pygame for the gui.

To play just start the GUI.py file and it should run. You need python3.
As for the buttons used, to change the orientation of the ships you can press W (vertical) and S (horizontal), click to place or shoot. 
The game also features 3 AI-s, which have to be manually changed in code. That can be done easily tho, you just go in GUI.py and change
the computerPlayer variable at the end of the file (line 120) from ComputerPlayers.ProbabilityAI(playerBoard, computerBoard, 2, 5, 16, 4, 2, 9) to ComputerPlayers.BetterAI(playerBoard, computerBoard)
or ComputerPlayers.AI(playerBoard, computerBoard)

You can also play with the quotas from the ProbabilityAI, which are the numbers 2, 5, 16, 4, 2, 9. Some values might make the AI very dumb because the way that AI works
is by trying to fit ships in each square, and based on those quotas increasing or decreasing the probability of a ship being there or not
The numbers 2, 5, 16, 4, 2 and 9 for the quotas were found by using a very basic regression in which i let 2 AI's play against each other for like 1000 times
with random quotas and then lowering the quota range to be closer and closer to the best ones. Then i just rounded them to end up with integers.

To replay, you have to restart the game.

This was made as a proof of concept for myself but if it gets some traction then i might try and make it better
