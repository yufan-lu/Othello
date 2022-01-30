

class GameController:
    """game controller(singleton), storing information concerning the status
    of game and number of disks with different colors"""
    def __init__(self, WIDTH, HEIGHT):
        self.black_cnt = 0
        self.white_cnt = 0
        self.black_win = False
        self.white_win = False
        self.draw = False
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPACE = 70

    def update(self):
        """when the game ends, display the game information
        and the result at the board"""
        fill(255, 0, 0)
        textSize(50)
        if (self.black_win or self.white_win or self.draw):
            text("BLACK: " + str(self.black_cnt),
                 self.WIDTH/2 - self.SPACE * 2, self.HEIGHT/2 - self.SPACE)
            text("WHITE: " + str(self.white_cnt),
                 self.WIDTH/2 - self.SPACE * 2, self.HEIGHT/2)
            if (self.black_win):
                text("BLACK WINS", self.WIDTH/2 - self.SPACE * 2,
                     self.HEIGHT/2 + self.SPACE)
            if (self.white_win):
                text("WHITE WINS", self.WIDTH/2 - self.SPACE * 2,
                     self.HEIGHT/2 + self.SPACE)
            if (self.draw):
                text("DRAW", self.WIDTH/2 - self.SPACE * 2,
                     self.HEIGHT/2 + self.SPACE)
