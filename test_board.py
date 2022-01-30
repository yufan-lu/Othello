from board import Board
from disk import Disk
from game_controller import GameController


def test_board_constructor():
    gc = GameController(100, 100)
    board = Board(100, 100, 100, 1, gc)
    assert board.disks[0][0] is None

    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    assert len(board.disks) == 4
    assert len(board.disks[0]) == 4
    assert board.disks[0][0] is None
    assert board.disks[1][1].if_black is False
    assert board.disks[1][2].if_black is True


def test_set_disks():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    board.set_disk(150, 50)
    assert board.disks[0][1] is not None
    assert board.disks[0][1].if_black is True
    board.set_disk(250, 50)
    assert board.disks[0][2] is not None
    assert board.disks[0][2].if_black is False


def test_check_winner():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)

    board.disk_cnt = 16
    board.blk_cnt = 9
    board.wht_cnt = 7
    board.check_winner()
    assert board.gc.black_win is True
    assert board.gc.black_cnt == 9
    assert board.gc.white_cnt == 7

    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)
    board.disk_cnt = 15
    board.blk_cnt = 8
    board.wht_cnt = 7
    board.check_winner()
    assert board.gc.black_win is False
    assert board.gc.black_cnt != 8
    assert board.gc.white_cnt != 7


def test_legal():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)

    assert board.legal(1, 1) is False
    assert board.legal(1, 0) is True
    board.set_disk(50, 100)
    assert board.legal(1, 0) is False


def test_legal_steps():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)

    legal_steps = board.legal_steps
    assert (1, 0) in legal_steps
    assert (0, 0) not in legal_steps
    assert (3, 2) in legal_steps


def test_flip():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)

    board.flip(0, 1)
    assert board.disks[1][1].if_black is True


def test_best_legal_step():
    gc = GameController(400, 400)
    board = Board(400, 400, 100, 4, gc)

    assert board.best_legal_step == (0, 1)

    board.set_disk(100, 0)
    assert board.best_legal_step == (0, 2)
