import pygame
import Board
import sys
import Game
import ComputerPlayers

class GUI:
    def __init__(self, game: Game.Game):
        pygame.init()
        self._game = game
        self._BLACK = (0, 0, 0)
        self._WHITE = (255, 255, 255)
        self._GREEN = (0, 255, 0)
        self._BLUE = (0, 0, 255)
        self._RED = (255, 0, 0)
        self._GRAY = (128, 128, 128)
        self._colorDict = {' ': self._BLUE, '[]': self._GRAY, '/': self._WHITE, 'X': self._RED}
        self._SQUARESIZE = SQUARESIZE = 50
        self._COL_COUNT = self._ROW_COUNT = 8
        self._width = SQUARESIZE * self._COL_COUNT * 2 + SQUARESIZE
        self._height = SQUARESIZE * self._ROW_COUNT + SQUARESIZE
        size = (self._width, self._height)

        self._screen = pygame.display.set_mode(size)
        self.draw_board(self._game.boards())

    def draw_board(self, board):
        self._screen.fill(self._BLUE)
        myBoard = board.myBoard
        hitBoard = board.hitBoard
        for column in range(self._COL_COUNT):
            for row in range(self._ROW_COUNT):
                pygame.draw.rect(self._screen, self._BLACK, (column * self._SQUARESIZE, row * self._SQUARESIZE+self._SQUARESIZE, self._SQUARESIZE, self._SQUARESIZE))
                pygame.draw.rect(self._screen, self._colorDict[myBoard[row * 8 + column]],
                                 (column * self._SQUARESIZE + 1, row * self._SQUARESIZE+self._SQUARESIZE + 1, self._SQUARESIZE - 2, self._SQUARESIZE - 2))

                pygame.draw.rect(self._screen, self._BLACK, (self._SQUARESIZE * self._COL_COUNT + self._SQUARESIZE + column * self._SQUARESIZE, row * self._SQUARESIZE+self._SQUARESIZE, self._SQUARESIZE, self._SQUARESIZE))
                pygame.draw.rect(self._screen, self._colorDict[hitBoard[row * 8 + column]],
                                 (self._SQUARESIZE * self._COL_COUNT + self._SQUARESIZE + column * self._SQUARESIZE + 1, row * self._SQUARESIZE + self._SQUARESIZE + 1,
                                  self._SQUARESIZE - 2, self._SQUARESIZE - 2))

    def start(self):
        pygame.display.set_caption("Battleships")

        clock = pygame.time.Clock()

        phase = 'prep'
        ships = ['battleship', 'cruiser', 'destroyer']
        idx = 2
        orientation = 'H'
        player = True
        gameTime = True

        while True:
            if idx == -1:
                phase = 'game'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if gameTime:
                    if event.type == pygame.KEYDOWN and phase == 'prep':
                        if event.key == pygame.K_w:
                            orientation = 'V'
                        if event.key == pygame.K_s:
                            orientation = 'H'

                    if event.type == pygame.MOUSEBUTTONDOWN and phase == 'prep':
                        ship = ships[idx]
                        coordinates = pygame.mouse.get_pos()
                        try:
                            self._game.player_place(str(coordinates[1] // self._SQUARESIZE - 1),
                                                    chr(coordinates[0] // self._SQUARESIZE + ord('A')), ship, orientation)
                            idx -= 1
                            self.draw_board(self._game.boards())
                        except ValueError:
                            pass
                        except Exception as e:
                            print(e)

                    if event.type == pygame.MOUSEBUTTONDOWN and phase == 'game':
                        coordinates = pygame.mouse.get_pos()
                        try:
                            self._game.player_hit(str(coordinates[1] // self._SQUARESIZE - 1),
                                                  chr(coordinates[0] // self._SQUARESIZE + ord('A') - 9))
                            if self._game.is_finished():
                                gameTime = False
                                player = True
                            self._game.computer_hit()
                            if self._game.is_finished() and gameTime:
                                gameTime = False
                                player = False
                        except ValueError:
                            pass
                        except Exception as e:
                            print(e)
                        self.draw_board(self._game.boards())
                else:
                    font = pygame.font.Font('freesansbold.ttf', 32)

                    if player:
                        text = font.render('Player wins!', True, self._BLACK)

                    else:
                        text = font.render('Computer wins!', True, self._BLACK)
                    textRect = text.get_rect()

                    textRect.center = (self._width // 2, self._height // 2)

                    self._screen.blit(text, textRect)

            pygame.display.flip()

            clock.tick(60)


playerBoard = Board.Board()
computerBoard = Board.Board()
computerPlayer = ComputerPlayers.ProbabilityAI(playerBoard, computerBoard, 2, 5, 16, 4, 2, 9)
# computerPlayer = ComputerPlayers.BetterAI(playerBoard, computerBoard)
game = Game.Game(playerBoard, computerBoard, computerPlayer)
gui = GUI(game)
gui.start()
