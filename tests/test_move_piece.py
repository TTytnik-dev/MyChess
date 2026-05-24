import pytest
from app.src.board import Board
from app.src.fen import parse_fen
from app.src.pieces import Piece, Pawn, Knight, Bishop, King, Queen, Rook


def test_move_piece():
    test_board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    test_board.move_piece(6, 3, 4, 3)
    assert test_board.board[4][3] is not None
    assert test_board.board[6][3] is None
    assert isinstance(test_board.board[4][3], Pawn)

    test_board = parse_fen(
        "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    )
    test_board.move_piece(4, 4, 3, 3)
    assert test_board.board[4][4] is None
    assert (
        isinstance(test_board.board[3][3], Pawn)
        and test_board.board[3][3].color == "white"
    )

    test_board = parse_fen(
        "rnbqkb1r/ppp1pppp/5n2/8/8/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 0 1"
    )
    test_board.move_piece(2, 5, 4, 6)
    assert test_board.board[2][5] is None
    assert test_board.board[4][6] is not None
    assert isinstance(test_board.board[4][6], Knight)

    test_board.move_piece(7, 5, 4, 2)
    assert test_board.board[7][5] is None
    assert test_board.board[4][2] is not None
    assert isinstance(test_board.board[4][2], Bishop)

    test_board = parse_fen("r3k2r/ppp1p1pp/2Np4/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    test_board.move_piece(7, 4, 7, 6)
    assert test_board.board[7][4] is None
    assert isinstance(test_board.board[7][6], King)
    assert isinstance(test_board.board[7][5], Rook)

    test_board = parse_fen("8/kPK5/8/8/8/8/8/8 w - - 0 1")
    test_board.move_piece(1, 1, 0, 1, "q")
    assert test_board.board[1][1] is None
    assert isinstance(test_board.board[0][1], Queen)

    test_board = parse_fen(
        "q3kb1r/1pp1pppp/2n1b3/8/2B3n1/2N2N2/1PPP1PPP/2BQK2R w Kk - 0 1"
    )
    assert not test_board.move_piece(0, 0, 4, 0)
    assert not test_board.move_piece(7, 7, 7, 3)
    assert not test_board.move_piece(7, 7, 6, 7)
    assert not test_board.move_piece(7, 0, 5, 7)
    assert not test_board.move_piece(7, 4, 5, 4)

    with pytest.raises(Exception):
        test_board.move_piece(7, 7, 7, 7)

    with pytest.raises(Exception):
        test_board.move_piece(8, 0, 7, 7)

    with pytest.raises(Exception):
        test_board.move_piece(0, 0, 8, 7)
