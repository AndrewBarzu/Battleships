from texttable import Texttable


class Board:
    def __init__(self):
        self._board = [' '] * 64
        self._hits = 0


    def _validate_placement(self, x, y, shipType, orientation):
        sizes = {'destroyer': 2, 'cruiser': 3, 'battleship': 4}
        orientations = {'H': y, 'V': x}
        if orientations[orientation] + sizes[shipType] > 8:
            raise ValueError("Ship does not fit")

        for i in range(sizes[shipType]):
            if orientation == 'V':
                if self._board[8 * (x + i) + y] == '[]':
                    raise ValueError("Ship overlaps")
            else:
                if self._board[8 * x + y + i] == '[]':
                    raise ValueError("Ship overlaps")

    def place(self, x, y, shipType, orientation):
        sizes = {'destroyer': 2, 'cruiser': 3, 'battleship': 4}
        self._validate_placement(x, y, shipType, orientation)

        for i in range(sizes[shipType]):
            if orientation == 'V':
                self._board[8 * (x+i) + y] = '[]'
            else:
                self._board[8 * x + y+i] = '[]'

    def hit(self, x, y):
        if self._board[8*x + y] == '[]':
            self._hits += 1
            self._board[8*x + y] = 'X'
            return True
        elif self._board[8*x + y] == ' ':
            self._board[8 * x + y] = '/'
            return False
        else:
            raise ValueError('Already attacked there')

    def __str__(self):
        table = Texttable()
        for i in range(8):
            row = [self._board[8 * i + y] for y in range(8)]
            table.add_row(row)
        return table.draw()
    
    def myBoard(self):
        return [self._board[i] for i in range(len(self._board))]

    def display_for_enemy(self):
        table = Texttable()
        for i in range(8):
            row = [self._board[8 * i + y] if self._board[8 * i + y] != '[]' else ' ' for y in range(8)]
            table.add_row(row)
        return table.draw()

    @property
    def hits(self):
        return self._hits

    @property
    def board(self):
        return [self._board[i] if self._board[i] != '[]' else ' ' for i in range(len(self._board))]

