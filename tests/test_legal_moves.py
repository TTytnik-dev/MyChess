import pytest
from app.src.board import Board
from app.src.fen import parse_fen

def test_legal_moves():

    test_board = parse_fen("5rk1/2p2p1p/1p4p1/p1b5/8/1P2NPP1/P6P/3R2K1 w - - 0 1")
    moves = test_board.get_legal_moves(5, 4)
    assert(len(moves) == 0)

    test_board = parse_fen("6k1/2p2p1p/1p4p1/pb6/6N1/1P2RPP1/r6P/6K1 w - - 0 1")
    moves = test_board.get_legal_moves(7, 6)
    assert(len(moves) == 1)
    assert([7,7] in moves)

    test_board = parse_fen("6k1/2p2p1p/1p4p1/p1b5/6N1/1P3PP1/r6P/4R1K1 w - - 0 1")
    moves = test_board.get_legal_moves(4, 6)
    assert(len(moves) == 2)
    assert([6,5] in moves)
    assert ([5, 4] in moves)

    test_board = parse_fen("r3k2r/ppp1p1pp/2Np4/8/8/8/PPPPPPPP/R1BQK1NR b KQkq - 0 1")
    moves = test_board.get_legal_moves(0, 4)
    assert(len(moves) == 4)
    assert([1, 3] in moves)
    assert([0, 5] in moves)
    assert([0, 6] in moves)
    assert([1, 5] in moves)

    test_board = parse_fen("r3k2r/ppp1p1pp/2Np4/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    moves = test_board.get_legal_moves(7, 4)
    assert(len(moves) == 4)
    assert([7, 3] in moves)
    assert([7, 5] in moves)
    assert([7, 2] in moves)
    assert([7, 6] in moves)
