
class Disk:
    """Disk class(prototype), representing a chess piece"""
    def __init__(self, if_black, row, col, CELL_SIZE):
        self.if_black = if_black
        self.DISK_WIDTH = 90
        self.DISK_HEIGHT = 90
        self.BLK_BASE = 0
        self.WHT_BASE = 255
        self.CELL_SIZE = CELL_SIZE
        self.row = row
        self.col = col

    def flip(self):
        """reverse the color"""
        self.if_black = not self.if_black

    def display(self):
        """display the disk at the board"""
        fill(self.BLK_BASE if self.if_black else self.WHT_BASE)
        ellipse((self.col + 0.5) * self.CELL_SIZE,
                (self.row + 0.5) * self.CELL_SIZE,
                self.DISK_WIDTH, self.DISK_HEIGHT)
