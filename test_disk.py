from disk import Disk


def test_flip():
    disk = Disk(True, 0, 0, 100)
    assert disk.if_black is True
    disk.flip()
    assert disk.if_black is False
