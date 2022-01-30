from board import Board
from game_controller import GameController
from ai import AI


def test_constructor():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    ai = AI(board)

    assert ai.board is board
    assert ai.board.gc is gc


def test_find_best_legal_step():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    ai = AI(board)

    best_step = ai.find_best_legal_step()
    assert best_step == (100, 0)
    assert ai.set_disk(best_step[0], best_step[1]) is True
    best_step = ai.find_best_legal_step()
    assert best_step == (200, 0)
    assert ai.set_disk(best_step[0], best_step[1]) is True
