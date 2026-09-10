import unittest
from contextlib import ExitStack
from unittest.mock import Mock, patch

from app.gui import window
from app.src.board import Board
from app.src.pieces import Pawn


class TestBoardFlipGUI(unittest.TestCase):
    def run_clicks(self, positions):
        frames = []
        mouse_position = (900, 420)
        clicks = iter(positions)

        def events():
            nonlocal mouse_position
            try:
                position = next(clicks)
            except StopIteration:
                return [window.pygame.event.Event(window.pygame.QUIT)]
            if position is None:
                return []
            mouse_position = position
            return [window.pygame.event.Event(window.pygame.MOUSEBUTTONDOWN, button=1)]

        def record_frame(screen, board, flipped):
            frames.append((flipped, window.board_to_fen(board)))

        with ExitStack() as stack:
            for target in (
                'pygame.init', 'pygame.quit', 'pygame.display.set_mode',
                'pygame.display.flip', 'pygame.key.set_repeat',
                'pygame.scrap.init', 'pygame.time.set_timer',
                'load_images', 'Stockfish',
            ):
                stack.enter_context(patch(f'app.gui.window.{target}'))
            for name in vars(window):
                if name.startswith('draw_'):
                    stack.enter_context(patch.object(window, name))
            stack.enter_context(patch.object(window, 'draw_pieces', side_effect=record_frame))
            stack.enter_context(patch.object(window.pygame.event, 'get', side_effect=events))
            stack.enter_context(patch.object(
                window.pygame.mouse, 'get_pos', side_effect=lambda: mouse_position
            ))
            with self.assertRaises(SystemExit) as stopped:
                window.main()
            self.assertIn(stopped.exception.code, (None, 0))
        return frames

    def test_piece_rendering_when_flipped(self):
        board = Board()
        pawn = Pawn(2, 1, "white")
        board.put_piece(2, 1, pawn)
        screen = Mock()
        pawn_image = object()

        with patch.dict(window.IMAGES, {"wP": pawn_image}, clear=True):
            for flipped, expected_position in [
                (False, (100, 200)),
                (True, (600, 500)),
                (False, (100, 200)),
            ]:
                with self.subTest(flipped=flipped, position=expected_position):
                    screen.reset_mock()
                    window.draw_pieces(screen, board, flipped)
                    screen.blit.assert_called_once_with(
                        pawn_image, window.pygame.Rect(*expected_position, 100, 100)
                    )
                    self.assertIs(board.board[2][1], pawn)
                    self.assertEqual((pawn.y, pawn.x), (2, 1))

    def test_flip_button_toggles_and_restores_orientation(self):
        frames = self.run_clicks([None, (900, 420), (900, 420)])
        self.assertEqual([flipped for flipped, _ in frames], [False, True, False])
        self.assertEqual(frames[0][1], frames[1][1])
        self.assertEqual(frames[0][1], frames[2][1])

    def test_mouse_move_e2_e4_on_flipped_board(self):
        frames = self.run_clicks([(900, 420), (350, 150), (350, 350)])
        self.assertEqual([flipped for flipped, _ in frames], [True, True, True])
        self.assertEqual(frames[0][1], frames[1][1])
        board = window.parse_fen(frames[-1][1])
        self.assertIsNone(board.board[6][4])
        pawn = board.board[4][4]
        self.assertIsNotNone(pawn)
        self.assertEqual(type(pawn).__name__, 'Pawn')
        self.assertEqual(pawn.color, 'white')
        self.assertEqual(board.who_moves, 'black')
