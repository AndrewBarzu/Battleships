from Game import Game

class UI:
    def __init__(self, game: Game):
        self._game = game

    def start(self):
        for ship in [ 'destroyer', 'cruiser', 'battleship']:
            while True:
                print('Place ' + ship + ' at coordinates')
                coordinates = input('(x, y)> ')
                coordinates = coordinates.split(' ')
                if len(coordinates) != 2:
                    print('Bad coordinates')
                    continue
                orientation = input('Oriented {"V" for vertical and "H" for horizontal}: ')
                try:
                    self._game.player_place(coordinates[0], coordinates[1], ship, orientation)
                except ValueError as e:
                    print(e)
                    continue
                break

        player = True
        while not self._game.is_finished():
            try:
                if player:
                    coordinates = input('(x, y)> ')
                    coordinates = coordinates.split(' ')
                    if len(coordinates) != 2:
                        print('Bad coordinates')
                        continue
                    self._game.player_hit(coordinates[0], coordinates[1])
                else:
                    self._game.computer_hit()
                    boards = self._game.printable_boards()
                    print("Hit Board: \n" + boards.hitBoard)
                    print("Your Board: \n" + boards.myBoard)
                player = not player
            except Exception as e:
                print(e)
                continue

        if not player:
            print("Player wins!")
        else:
            print("Computer wins!")
