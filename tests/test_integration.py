import unittest
from app.src.fen import parse_fen


class TestGameScenarios(unittest.TestCase):

    def test_scholars_mate(self):
        board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        board.move_piece(6, 4, 4, 4)
        board.move_piece(1, 4, 3, 4)

        board.move_piece(7, 5, 4, 2)
        board.move_piece(0, 1, 2, 2)

        board.move_piece(7, 3, 3, 7)
        board.move_piece(0, 6, 2, 5)

        board.move_piece(3, 7, 1, 5)

        game_over = board.check_game_over()

        self.assertTrue(game_over)
        self.assertEqual(board.game_over_status, "white_win_checkmate")

    def test_lose_castling_rights(self):
        board = parse_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        self.assertIn([7, 2], board.get_legal_moves(7, 4))

        board.move_piece(7, 0, 6, 0)

        board.move_piece(0, 7, 1, 7)

        board.move_piece(6, 0, 7, 0)

        board.move_piece(1, 7, 0, 7)

        self.assertNotIn([7, 2], board.get_legal_moves(7, 4))

    def test_pawn_promotion(self):

        board = parse_fen("8/3P4/8/8/8/8/8/k6K w - - 0 1")

        board.move_piece(1, 3, 0, 3, promotion="q")

        piece = board.board[0][3]
        self.assertIsNotNone(piece)
        self.assertEqual(type(piece).__name__, "Queen")
        self.assertEqual(piece.color, "white")