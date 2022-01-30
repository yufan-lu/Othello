from game_character import GameCharacter


class AI(GameCharacter):
    """AI class(singleton)"""
    def __init__(self, board):
        self.board = board

    def find_best_legal_step(self):
        """find the best legal step, return the coordinates at the board"""
        step = self.board.best_legal_step
        x = step[1] * self.board.CELL_SIZE
        y = step[0] * self.board.CELL_SIZE
        return (x, y)
