import pytest
from app.src.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from app.src.board import Board
from app.src.fen import parse_fen

def test_pawn_moves():
    test_board = parse_fen("rnbqkbnr/p1p1p1pp/8/8/3p4/1p3p2/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    moves_1 = test_board.board[6][4].get_valid_moves(test_board)

    assert len(moves_1) == 3
    assert [5, 5] in moves_1
    assert [5, 4] in moves_1
    assert [4, 4] in moves_1

    moves_2 = test_board.board[6][3].get_valid_moves(test_board)
    assert len(moves_2) == 1
    assert [5, 3] in moves_2

    moves_3 = test_board.board[6][1].get_valid_moves(test_board)
    assert len(moves_3) == 0

def test_queen_moves():
    test_board = parse_fen("rn2kb1r/pp2pppp/2p5/3q1b2/8/3P4/PPP2PPP/R1BQKBNR w KQkq - 0 1")
    moves = test_board.board[3][3].get_valid_moves(test_board)

    assert len(moves) == 16
    assert [6, 0] in moves
    assert [6, 6] in moves
    assert [5, 3] in moves
    assert [0, 3] in moves
    assert [3, 5] not in moves
    assert [2, 4] in moves
    assert [2, 2] not in moves

def test_rook_moves():
    test_board = parse_fen("6k1/p1pn2pp/8/3R4/2P1rp2/8/PP3PPP/4R1K1 w - - 0 1")
    moves = test_board.board[4][4].get_valid_moves(test_board)
    assert len(moves) == 9
    assert [3, 6] not in moves
    assert [4, 5] not in moves
    assert [4, 2] in moves
    assert [4, 3] in moves
    assert [7, 4] in moves
    assert [1, 4] in moves

def test_bishop_moves():
    test_board = parse_fen("6k1/p1pn1ppp/8/3B4/2P1rp2/8/PP3PPP/4R1K1 w - - 0 1")
    moves = test_board.board[3][3].get_valid_moves(test_board)
    assert len(moves) == 6
    assert [4, 4] in moves
    assert [4, 2] not in moves
    assert [1, 5] in moves
    assert [1, 1] in moves
    assert [2, 3] not  in moves

def test_knight_moves():
    test_board = parse_fen("r1bqkb1r/ppp1nppp/2n1p3/3pP3/3P4/5N2/PPP2PPP/RNBQKB1R w KQkq - 0 1")
    moves = test_board.board[2][2].get_valid_moves(test_board)
    assert len(moves) == 5
    assert [0, 1] in moves
    assert [3, 0] in moves
    assert [3, 4] in moves
    assert [4, 3] in moves
    assert [4, 1] in moves

def test_king_moves():
    test_board = parse_fen("r1bqkb1r/ppp1nppp/4p3/3pP3/3P4/5N2/PPP1KnPP/RNBQ3R w kq - 0 1")
    moves = test_board.board[6][4].get_valid_moves(test_board)

    assert len(moves) == 6

    assert [6, 3]  in moves
    assert [6, 5] in moves
    assert [5, 3] in moves
    assert [7, 5] in moves
    assert [5, 4] in moves
    assert [7, 4] in moves

