from game_controller import GameController


def test_constructor():
    gc = GameController(400, 400)

    assert gc.black_cnt == 0
    assert gc.white_cnt == 0
    assert gc.black_win is False
    assert gc.white_win is False
    assert gc.draw is False
    assert gc.WIDTH == 400
    assert gc.HEIGHT == 400
