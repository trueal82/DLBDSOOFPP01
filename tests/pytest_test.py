import pytest


def test_passed() -> None:
    assert (1, 2, 3) == (1, 2, 3)


@pytest.mark.xfail()
def test_fail() -> None:
    assert (1, 2, 3) == (3, 2, 1)
