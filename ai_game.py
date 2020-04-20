from Board import Board
from ComputerPlayers import BetterAI, AI, ProbabilityAI


class AiGame:
    def __init__(self):
        self._player1Board = Board()
        self._player2Board = Board()
        self._player1 = ProbabilityAI(self._player2Board, self._player1Board, 2, 5, 16, 4, 2, 9)
        # self._player1 = ProbabilityAI(self._player2Board, self._player1Board, 1, 5, 25, 4, 6, 8)
        # self._player1 = ProbabilityAI(self._player2Board, self._player1Board, 1, 5, 25, 40, 20, 20)
        # self._player2 = ProbabilityAI(self._player1Board, self._player2Board, 1, 5, 25, 4, 6, 8)
        # self._player1 = BetterAI(self._player2Board, self._player1Board)
        # self._player2 = ProbabilityAI(self._player1Board, self._player2Board, 2, 5, 16, 4, 2, 9)
        # self._player2 = BetterAI(self._player1Board, self._player2Board)
        # self._player1 = AI(self._player2Board, self._player1Board)
        self._player2 = AI(self._player1Board, self._player2Board)
        self._player1.place()
        self._player2.place()

    def hit(self, player):
        if player is True:
            self._player1.take_shot()
        else:
            self._player2.take_shot()

    def is_finished(self):
        return self._player1Board.hits == 9 or self._player2Board.hits == 9

    def print_boards(self):
        return str(self._player1Board), str(self._player2Board)

median = 0
player1wins = 0
player2wins = 0

for i in range(1000):
    game = AiGame()
    count = 0
    myPlayer = False
    while not game.is_finished():
        myPlayer = not myPlayer
        if myPlayer:
            game.hit(myPlayer)
        else:
            game.hit(myPlayer)
        count += 1
    if myPlayer:
        player1wins += 1
    else:
        player2wins += 1
    median += count

print(median/1000/2, player1wins, player2wins)
