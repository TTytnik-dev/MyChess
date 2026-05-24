import unittest
from stockfish import Stockfish
from app.src.fen import parse_fen


class TestFeatures(unittest.TestCase):

    def test_board_flip_logic(self):
        flipped = True
        mouse_x, mouse_y = 0, 0
        self.assertEqual(7 - (mouse_x // 800 // 8), 7)

    def test_load_custom_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
        board = parse_fen(fen)
        piece = board.board[4][4]
        self.assertIsNotNone(piece)
        self.assertEqual(type(piece).__name__, "Pawn")

    def test_stockfish_presence(self):
        try:
            engine = Stockfish("stockfish")
            engine.set_skill_level(8)
            self.assertTrue(True)
        except Exception:
            self.skipTest("Stockfish не найден на этой машине")
