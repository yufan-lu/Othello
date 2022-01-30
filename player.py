from game_character import GameCharacter


class Player(GameCharacter):
    """Player class(singleton)"""
    def __init__(self, board):
        self.board = board
