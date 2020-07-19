from UI import UI
from Game import Game
from ComputerPlayers import BetterAI, ProbabilityAI
from Board import Board

class AppStart:
    def __init__(self, interface):
        self._interface = interface
        self._interface.start()

if __name__ == "__main__":
    interface = input("Interface > ")
    playerBoard = Board()
    computerBoard = Board()
    computerPlayer = BetterAI(playerBoard, computerBoard)
    game = Game(playerBoard, computerBoard, computerPlayer)
    if interface == 'ui':
        ui = UI(game)
        AppStart(ui)