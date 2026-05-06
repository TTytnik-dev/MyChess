import pytest
from app.src.fen import parse_fen
from app.src.pieces import Pawn, Rook, Knight, Bishop, Queen, King

@pytest.mark.parametrize("fen", [
    " ",
    "rnbqkbnr/pppppppp w KQkq - 0 1",
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 -2 2",
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 -2",
    "8/8/8/3m4/8/5K2/8/8 w - - 0 10",
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KPkq c3 0 2",
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KkqK c3 0 2",
    "8/8/8/34/8/5K2/8/8 w - - 0 10",
    "8/8/8/342/8/5K2/8/8 w - - 0 10",
    "rnbqknr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KkqK c3 0 2",
    "rnbqknr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR B KkqK c3 0 2",
    "rnbqknr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR Q KkqK c3 0 2",
])

def test_invalid_fen(fen):
    with pytest.raises(Exception):
        parse_fen(fen)


def test_initial_board_setup():
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    startBoard = parse_fen(start_fen)

    assert startBoard.WhoMoves == "white"

    assert startBoard.board[0][0].color == "black"
    assert startBoard.board[7][7].color == "white"
    assert (isinstance(startBoard.board[7][7], Rook))
    assert isinstance(startBoard.board[1][4],Pawn)

    fen = "rnbqkbnr/pppp1ppp/8/4p3/5P2/8/PPPPP1PP/RNBQKBNR b KQkq f3 0 2"
    board = parse_fen(fen)

    assert board.WhoMoves == "black"

    e5_square = board.board[3][4]
    assert isinstance(e5_square, Pawn)
    assert e5_square.color == "black"

    f4_square = board.board[4][5]
    assert isinstance(f4_square, Pawn)
    assert f4_square.color == "white"

    assert board.board[1][4] is None

    assert board.board[6][5] is None

    b8_square = board.board[0][1]
    assert isinstance(b8_square, Knight)
    assert b8_square.color == "black"

