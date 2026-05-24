from app.src.board import Board
import pytest
from app.src.fen import parse_fen


def test_game_over():
    test_board = parse_fen("8/6b1/8/8/8/q2k4/8/1K6 w - - 0 1")
    assert test_board.check_game_over()

    test_board = parse_fen("8/6b1/8/8/8/q2k4/7Q/1K6 w - - 0 1")
    assert not test_board.check_game_over()

    test_board = parse_fen("8/6b1/8/8/8/q2k4/8/1K6 b - - 0 1")
    assert not test_board.check_game_over()

    test_board = parse_fen("8/8/8/8/8/3k4/1q6/1K6 w - - 0 1")
    assert not test_board.check_game_over()

    test_board = parse_fen("8/8/8/8/8/2k5/1q6/1K6 w - - 0 1")
    assert test_board.check_game_over()

    test_board = parse_fen("1q3k2/r7/8/8/8/8/6Q1/K7 w - - 0 1")
    assert not test_board.check_game_over()

    test_board = parse_fen("1q3k2/r7/8/8/8/8/5B2/K7 w - - 0 1")
    assert not test_board.check_game_over()

    test_board = parse_fen("7R/k1p5/1n5r/8/8/5B2/R7/1K4B1 b - - 0 1")
    assert test_board.check_game_over()
