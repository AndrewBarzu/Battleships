from Board import Board
from ComputerPlayers import AI

class Game:
    def __init__(self, playerBoard: Board, computerBoard: Board, computerPlayer: AI):
        self._playerBoard = playerBoard
        self._computerBoard = computerBoard
        self._computerPlayer = computerPlayer
        self._computerPlayer.place()
        self._yvalues = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

    def player_place(self, x, y, shipType, orientation):
        if not x.isnumeric() or y not in self._yvalues:
            raise ValueError("Bad coordinates")
        x = int(x)
        if x not in range(8):
            raise ValueError("Bad coordinates")
        y = self._yvalues[y]
        if shipType not in ['cruiser', 'destroyer', 'battleship']:
            raise ValueError("Bad ship type")
        if orientation not in ['V', 'H']:
            raise ValueError("Bad orientation")
        self._playerBoard.place(x, y, shipType, orientation)

    def is_finished(self):
        return self._computerBoard.hits == 9 or self._playerBoard.hits == 9

    def player_hit(self, x, y):
        if not x.isnumeric() or y not in self._yvalues:
            raise ValueError("Coords should be int")
        x = int(x)
        y = self._yvalues[y]
        return self._computerBoard.hit(x, y)

    def computer_hit(self):
        self._computerPlayer.take_shot()
        
    def boards(self):
        class Boards:
            def __init__(self, myBoard, hitBoard):
                self._myBoard = myBoard
                self._hitBoard = hitBoard

            @property
            def myBoard(self):
                return self._myBoard

            @property
            def hitBoard(self):
                return self._hitBoard
        
        return Boards(self._playerBoard.myBoard(), self._computerBoard.board)

    def printable_boards(self):
        class Boards:
            def __init__(self, myBoard, hitBoard):
                self._myBoard = myBoard
                self._hitBoard = hitBoard

            @property
            def myBoard(self):
                return self._myBoard

            @property
            def hitBoard(self):
                return self._hitBoard

        return Boards(str(self._playerBoard), str(self._computerBoard.display_for_enemy()))
