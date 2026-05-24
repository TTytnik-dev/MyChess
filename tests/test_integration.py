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

        def test_en_passant_capture(self):
            board = parse_fen("4k3/3p4/8/4P3/8/8/8/4K3 b - - 0 1")

            board.move_piece(1, 3, 3, 3)

            self.assertIsNotNone(board.en_passant_target)
            self.assertEqual(board.en_passant_target.y, 3)
            self.assertEqual(board.en_passant_target.x, 3)

            board.move_piece(3, 4, 2, 3)

            self.assertEqual(type(board.board[2][3]).__name__, "Pawn")
            self.assertEqual(board.board[2][3].color, "white")
            self.assertIsNone(board.board[3][3])

        def test_fen_history_preservation(self):
            from app.src.fen import board_to_fen

            board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

            board.move_piece(6, 4, 4, 4)

            new_fen = board_to_fen(board)

            self.assertIn("KQkq", new_fen)

            self.assertIn("e3", new_fen)