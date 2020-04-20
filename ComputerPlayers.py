from Board import Board
import random

class AI:
    def __init__(self, hitBoard: Board, selfBoard: Board):
        self._hitBoard = hitBoard
        self._selfBoard = selfBoard
        self._takenHits = self._hitBoard.board

    def place(self):
        for ship in ['cruiser', 'destroyer', 'battleship']:
            while True:
                try:
                    x = random.randint(0, 7)
                    y = random.randint(0, 7)
                    orientation = random.choice(['V', 'H'])
                    self._selfBoard.place(x, y, ship, orientation)
                    break
                except Exception:
                    continue
        # self._selfBoard.place(0, 0, 'cruiser', 'H')
        # self._selfBoard.place(7, 0, 'battleship', 'H')
        # self._selfBoard.place(4, 7, 'destroyer', 'V')

    def take_shot(self):
        while True:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if self._takenHits[8*x + y] == ' ':
                hit = self._hitBoard.hit(x, y)
                if hit is True:
                    self._takenHits[8*x + y] = 'X'
                else:
                    self._takenHits[8*x + y] = '/'
                break

class BetterAI(AI):
    def __init__(self, hitBoard, selfBoard):
        super(BetterAI, self).__init__(hitBoard, selfBoard)
        self._near_stack = []
        self._hit_stack = []
        self._seekIndices = self._init_seek_indices()

    @staticmethod
    def _init_seek_indices():
        return [index if index // 8 % 2 == 0 else index+1 for index in range(0, 64, 2)]

    def place(self):
        super(BetterAI, self).place()

    @staticmethod
    def _valid_index(index):
        return 0 <= index < 8

    def _seek(self):
        while True:
            index = random.choice(self._seekIndices)
            if self._takenHits[index] == ' ':
                self._shoot(index=index)
                break

    def _shoot(self, index=None, x=None, y=None):
        if index is not None:
            myX = index // 8
            myY = index % 8
        else:
            myX = x
            myY = y
        hit = self._hitBoard.hit(myX, myY)
        if hit is True:
            self._takenHits[8 * myX + myY] = 'X'
            if self._valid_index(myX + 1):
                self._near_stack.append((myX + 1, myY))
            if self._valid_index(myX - 1):
                self._near_stack.append((myX - 1, myY))
            if self._valid_index(myY - 1):
                self._near_stack.append((myX, myY - 1))
            if self._valid_index(myY + 1):
                self._near_stack.append((myX, myY + 1))
        else:
            self._takenHits[8 * myX + myY] = '/'


    def _destroy(self):
        while len(self._near_stack) != 0:
            nextTarget = self._near_stack.pop()
            if self._takenHits[8 * nextTarget[0] + nextTarget[1]] == ' ':
                self._shoot(x=nextTarget[0], y=nextTarget[1])
                break
            else:
                pass


    def take_shot(self):
        if len(self._near_stack) == 0:
            self._seek()
        else:
            self._destroy()


class ProbabilityAI(AI):
    def __init__(self, hitBoard, selfBoard, quota, xquota, morexQuota, shipq1, shipq2, shipq3):
        super(ProbabilityAI, self).__init__(hitBoard, selfBoard)
        self._probabilityMap = [0] * 64
        self._ships = [2, 3, 4]
        self._quota = quota
        self._xquota = xquota
        self._morexQuota = morexQuota
        self._shipQuotas = {2: shipq1, 3: shipq2, 4: shipq3}

    def place(self):
        super(ProbabilityAI, self).place()

    @staticmethod
    def _valid_index(index):
        return 0 <= index < 64

    def _fitShip(self, x, y, ship, mainQuota, xquota, morexQuota):
        myQuotas = {2: 7.4, 3: 4.7, 4: 3.5}
        if self._valid_index(8 * x + y + ship-1):
            count = 0
            quota = mainQuota
            xcount = 0
            for i in range(ship):
                if self._takenHits[8 * x + y + i] == '/':
                    self._probabilityMap[8 * x + y + i] = 0
                    break
                if self._takenHits[8 * x + y + i] == 'X':
                    xcount += 1
                    quota = self._shipQuotas[ship]
                count += 1
                if xcount > 1:
                    quota = morexQuota
            if count == ship:
                for i in range(ship):
                    if self._takenHits[8 * x + y + i] == 'X':
                        self._probabilityMap[8 * x + y + i] = 0
                    if 8*x + y + i % 2 == 0:
                        self._probabilityMap[8 * x + y + i] += quota - 2
                    else:
                        self._probabilityMap[8 * x + y + i] += quota
        if self._valid_index(8 * (x + ship-1) + y):
            count = 0
            quota = mainQuota
            xcount = 0
            for i in range(ship):
                if self._takenHits[8 * (x + i) + y] == '/':
                    self._probabilityMap[8 * (x + i) + y] = 0
                    break
                if self._takenHits[8 * (x + i) + y] == 'X':
                    xcount += 1
                    quota = myQuotas[ship]
                count += 1
                if xcount > 1:
                    quota = morexQuota
            if count == ship:
                for i in range(ship):
                    if self._takenHits[8 * (x + i) + y] == 'X':
                        self._probabilityMap[8 * (x + i) + y] = 0
                    if 8 * (x + i) + y % 2 == 0:
                        self._probabilityMap[8 * (x + i) + y] += quota - 2
                    else:
                        self._probabilityMap[8 * (x + i) + y] += quota

    def _calculate_probability(self):
        # print(self._takenHits)
        # for index in range(64):
        #     if self._valid_index(index+3) and 4 in self._ships:
        #         if self._takenHits[index+1] == 'X' and self._takenHits[index+2] == 'X' and self._takenHits[index+3] == 'X' and self._takenHits[index] == 'X':
        #             self._ships.remove(4)
        #     elif self._valid_index(index + 3 * 8) and 4 in self._ships:
        #         if self._takenHits[index] == 'X' and self._takenHits[index+1*8] == 'X' and self._takenHits[index+2*8] == 'X' and self._takenHits[index+3*8] == 'X':
        #             self._ships.remove(4)
        #     elif self._valid_index(index+2) and 3 in self._ships:
        #         if self._takenHits[index+1] == 'X' and self._takenHits[index+2] == 'X' and self._takenHits[index] == 'X':
        #             self._ships.remove(3)
        #     elif self._valid_index(index + 2 * 8) and 3 in self._ships:
        #         if self._takenHits[index] == 'X' and self._takenHits[index+1*8] == 'X' and self._takenHits[index+2*8] == 'X':
        #             self._ships.remove(3)
        #     elif self._valid_index(index+1) and 2 in self._ships:
        #         if self._takenHits[index+1] == 'X' and self._takenHits[index] == 'X':
        #             self._ships.remove(2)
        #     elif self._valid_index(index + 1 * 8) and 2 in self._ships:
        #         if self._takenHits[index] == 'X' and self._takenHits[index+1*8] == 'X':
        #             self._ships.remove(2)
        #
        # mainQuota = len(self._ships) * 2
        # print(str(len(self._ships)))

        self._probabilityMap = [0] * 64
        for index in range(64):
            x = index // 8
            y = index % 8
            for ship in self._ships:
                self._fitShip(x, y, ship, self._quota, self._xquota, self._morexQuota)

    def take_shot(self):
        self._calculate_probability()


        maxProbability = 0
        mostProbablePosition = (0, 0)
        for index in range(64):
            x = index // 8
            y = index % 8
            if self._takenHits[index] == '/' or self._takenHits[index] == 'X':
                self._probabilityMap[index] = 0
            if self._probabilityMap[index] > maxProbability:
                maxProbability = self._probabilityMap[index]
                mostProbablePosition = (x, y)

        hit = self._hitBoard.hit(mostProbablePosition[0], mostProbablePosition[1])
        if hit:
            self._takenHits[8 * mostProbablePosition[0] + mostProbablePosition[1]] = 'X'
        else:
            self._takenHits[8 * mostProbablePosition[0] + mostProbablePosition[1]] = '/'

