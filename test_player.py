from player import Player
from board import Board
from game_controller import GameController


def test_constructor():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    player = Player(board)

    assert player.board is board
    assert player.board.gc is gc


def test_set_disk():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    player = Player(board)

    assert player.set_disk(0, 0) is False
    assert player.set_disk(200, 0) is False
    assert player.set_disk(100, 0) is True
