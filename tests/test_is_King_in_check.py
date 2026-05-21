import pytest
from app.src.board import Board
from app.src.fen import parse_fen

def test_is_King_in_check():

    test_board = parse_fen("6k1/p1pn2pp/8/3R4/2P2p2/8/PP3PPP/4r1K1 w - - 0 1")
    assert(test_board.is_in_check("white"))
    assert(not test_board.is_in_check("black"))

    test_board = parse_fen("rnb1kbnr/pppp1ppp/8/4p3/3P3q/4PP2/PPP3PP/RNBQKBNR w KQkq - 0 1")
    assert(test_board.is_in_check("white"))
    assert(not test_board.is_in_check("black"))

    test_board = parse_fen("r1b1kbnr/ppp2ppp/3p1q2/2P1p3/8/3nPPP1/PPP4P/RNBQKBNR w KQkq - 0 1")
    assert(test_board.is_in_check("white"))
    assert(not test_board.is_in_check("black"))

    test_board = parse_fen("rR2k2r/p3bp1p/3pnqp1/2P1p3/7N/3QPPPB/P1P4P/4K2R w Kkq - 0 1")
    assert(test_board.is_in_check("black"))
    assert(not test_board.is_in_check("white"))

    test_board = parse_fen("1b2k2r/p2P3p/4Bqp1/4p3/7N/3Q2P1/P1P2p1P/5K1R w k - 0 1")
    assert(test_board.is_in_check("black"))

    test_board = parse_fen("1b3k1r/p2P3p/4Bqp1/4p3/7N/3Q2P1/P1P2p1P/5K1R w - - 0 1")
    assert (not test_board.is_in_check("black"))
    assert(not test_board.is_in_check("white"))

    test_board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert (not test_board.is_in_check("black"))
    assert(not test_board.is_in_check("white"))

    test_board = parse_fen("r5k1/pR4pp/5n2/2b5/8/1P4P1/P4P1P/3r1RK1 w - - 0 1")
    assert (not test_board.is_in_check("black"))
    assert(not test_board.is_in_check("white"))

    test_board = parse_fen("rnbqk1nr/pppp1ppp/4p3/8/1b1P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    assert (test_board.is_in_check("white"))
    assert (not test_board.is_in_check("black"))

    test_board = parse_fen("k7/8/8/8/8/8/8/K6q w - - 0 1")
    assert (test_board.is_in_check("white"))
    assert (not test_board.is_in_check("black"))