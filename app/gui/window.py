import pygame
import sys
import os
from app.src.pieces import King
from app.src.fen import parse_fen, board_to_fen
import argparse
import random

IMAGES = {}

HEIGHT = 800
UI_WIDTH = 250
WIDTH = 800 + UI_WIDTH
SQ_Size = 800 // 8
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

def draw_board(screen):
    for y in range(8):
        for x in range(8):
            if ((y + x) % 2) == 0:
                pygame.draw.rect(screen, LIGHT, pygame.Rect(x * SQ_Size, y * SQ_Size, SQ_Size, SQ_Size))
            else:
                pygame.draw.rect(screen, DARK, pygame.Rect(x * SQ_Size, y * SQ_Size, SQ_Size, SQ_Size))


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']

    for piece in pieces:
        path = os.path.join("assets", "images", f"{piece}.png")

        try:
            image = pygame.image.load(path)
            IMAGES[piece] = pygame.transform.scale(image, (SQ_Size, SQ_Size))
        except Exception as e:
            print(f"Cant add {path}. Error: {e}")

def draw_pieces(screen, game_board):
    class_to_char = {
        'Pawn': 'P', 'Knight': 'N', 'Bishop': 'B',
        'Rook': 'R', 'Queen': 'Q', 'King': 'K'
    }

    for y in range(8):
        for x in range(8):
            piece = game_board.board[y][x]
            if piece is not None:
                if piece.color == "white":
                    color  = "w"
                else:
                    color = "b"
                piece_type = type(piece).__name__
                key = color + class_to_char[piece_type]

                screen.blit(IMAGES[key], pygame.Rect(x * SQ_Size, y * SQ_Size, SQ_Size, SQ_Size))


def draw_hints(screen, valid_moves):
    for move in valid_moves:
        y, x = move
        center_x = x * SQ_Size + SQ_Size // 2
        center_y = y * SQ_Size + SQ_Size // 2
        pygame.draw.circle(screen, (169, 169, 169), (center_x, center_y), SQ_Size // 10)



def draw_selected_highlight(screen, selected_square):
    if selected_square is not None:
        y, x = selected_square
        highlight_color = (255, 226, 142)
        pygame.draw.rect(screen, highlight_color, pygame.Rect(x * SQ_Size, y * SQ_Size, SQ_Size, SQ_Size))


def draw_turn_indicator(screen, board):
    if hasattr(board, 'game_over_status') and board.game_over_status:
        return

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 28, bold=True)

    if board.who_moves == "white":
        text = " White's Turn "
        text_color = (0, 0, 0)
        bg_color = (240, 217, 181)
    else:
        text = " Black's Turn "
        text_color = (255, 255, 255)
        bg_color = (181, 136, 99)

    text_surface = font.render(text, True, text_color)

    ui_x_start = HEIGHT + 20
    bg_rect = pygame.Rect(ui_x_start, 20, text_surface.get_width() + 20, text_surface.get_height() + 20)

    pygame.draw.rect(screen, bg_color, bg_rect, border_radius=5)
    screen.blit(text_surface, (ui_x_start + 10, 30))


def draw_history_indicator(screen, viewing_history, current_index, max_index):
    if not viewing_history:
        return

    pygame.font.init()
    font_main = pygame.font.SysFont('Arial', 24, bold=True)
    font_sub = pygame.font.SysFont('Arial', 18)

    text_main = font_main.render("VIEWING HISTORY", True, (255, 50, 50))

    text_sub = font_sub.render(f"Move: {current_index} / {max_index}", True, (200, 200, 200))

    ui_x = HEIGHT + 20
    ui_y_main = 100
    ui_y_sub = 130

    screen.blit(text_main, (ui_x, ui_y_main))
    screen.blit(text_sub, (ui_x, ui_y_sub))


def draw_timers(screen, white_time, black_time):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 24, bold=True)

    def format_time(seconds):
        if seconds < 0: seconds = 0
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    white_text = font.render(f"White: {format_time(white_time)}", True, (255, 255, 255))
    black_text = font.render(f"Black: {format_time(black_time)}", True, (200, 200, 200))

    ui_x = HEIGHT + 20
    screen.blit(white_text, (ui_x, 180))
    screen.blit(black_text, (ui_x, 220))


def draw_undo_button(screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20, bold=True)

    button_rect = pygame.Rect(HEIGHT + 20, 280, 160, 40)

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        color = (100, 100, 100)
    else:
         color =  (70, 70, 70)


    pygame.draw.rect(screen, color, button_rect, border_radius=5)

    text_surface = font.render("UNDO MOVE", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect

def draw_check_highlight(screen, board):
    current_color = board.who_moves

    king_y = None
    king_x = None

    for y in range(8):
        for x in range(8):
            if isinstance(board.board[y][x], King) and board.board[y][x].color == current_color:
                king_y = y
                king_x = x
                break

    if  board.is_in_check(current_color):
        red_square_rect = pygame.Rect(king_x * SQ_Size, king_y * SQ_Size, SQ_Size, SQ_Size)
        pygame.draw.rect(screen, (255, 0, 0), red_square_rect)


def draw_game_over_screen(screen, board):
    if  board.game_over_status:
        status = board.game_over_status
        message = ""
        if status == "white_win_checkmate":
            message = "Checkmate! White wins."
        elif status == "black_win_checkmate":
            message = "Checkmate! Black wins."
        elif status == "draw_stalemate":
            message = "Draw! Stalemate on the board."
        elif status == "draw_insufficient_material":
            message = "Draw (insufficient material)."
        elif status == "draw_fifty_move_rule":
            message = "Draw (50-move rule)."
        elif status == "draw_threefold_repetition":
            message = "Draw (threefold repetition)."
        elif status == "white_win_timeout":
            message = "Time out! White wins."
        elif status == "black_win_timeout":
            message = "Time out! Black wins."
        else:
            message = "Game Over."

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 48, bold=True)
        text_surface = font.render(message, True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)


def get_promotion_choice(screen, color):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    pieces_to_choose = ['Q', 'R', 'B', 'N']
    if color == "white":
        prefix = 'w'
    else:
        prefix = 'b'

    panel_width = 4 * SQ_Size + 50
    panel_height = SQ_Size + 20
    start_x = (HEIGHT - panel_width) // 2
    start_y = (HEIGHT - panel_height) // 2

    pygame.draw.rect(screen, (200, 200, 200), (start_x, start_y, panel_width, panel_height), border_radius=10)

    clickable_rects = []
    for i, p in enumerate(pieces_to_choose):
        img_key = prefix + p
        img = IMAGES[img_key]

        rect = pygame.Rect(start_x + 25 + i * SQ_Size, start_y + 10, SQ_Size, SQ_Size)
        screen.blit(img, rect)

        clickable_rects.append((rect, p.lower()))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, choice in clickable_rects:
                    if rect.collidepoint(mouse_pos):
                        return choice


def main(play_vs_bot = False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    load_images()

    game_board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    move_history = [board_to_fen(game_board)]
    current_history_index = 0
    viewing_history = False

    selected_square = None
    valid_moves = []

    white_time = 600
    black_time = 600

    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 1000)

    while True:
        if play_vs_bot and game_board.who_moves == "black" and not game_board.game_over_status and not viewing_history:
            all_possible_moves = []
            for y in range(8):
                for x in range(8):
                    piece = game_board.board[y][x]
                    if piece and piece.color == "black":
                        moves = game_board.get_legal_moves(y, x)
                        for target_y, target_x in moves:
                            all_possible_moves.append((y, x, target_y, target_x))

            if all_possible_moves:
                pygame.time.delay(500)

                start_y, start_x, end_y, end_x = random.choice(all_possible_moves)
                game_board.move_piece(start_y, start_x, end_y, end_x)
                game_board.check_game_over()

                new_fen = board_to_fen(game_board)
                move_history.append(new_fen)
                current_history_index = len(move_history) - 1

                pygame.event.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == TIMER_EVENT:
                if not game_board.game_over_status:
                    if game_board.who_moves == "white":
                        white_time -= 1
                        if white_time <= 0:
                            game_board.game_over_status = "black_win_timeout"
                    else:
                        black_time -= 1
                        if black_time <= 0:
                            game_board.game_over_status = "white_win_timeout"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if current_history_index > 0:
                        current_history_index -= 1
                        viewing_history = True
                elif event.key == pygame.K_RIGHT:
                    if current_history_index < len(move_history) - 1:
                        current_history_index += 1
                        if current_history_index == len(move_history) - 1:
                            viewing_history = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                undo_button_rect = pygame.Rect(HEIGHT + 20, 280, 160, 40)
                if undo_button_rect.collidepoint((mouse_x, mouse_y)):
                    if play_vs_bot:
                        steps_to_undo = 2
                    else:
                        steps_to_undo = 1
                    if len(move_history) > steps_to_undo:
                        for _ in range(steps_to_undo):
                            move_history.pop()
                        current_history_index = len(move_history) - 1
                        game_board = parse_fen(move_history[current_history_index])
                        viewing_history = False
                        selected_square = None
                        valid_moves = []
                    continue

                if game_board.game_over_status or viewing_history:
                    continue
                if mouse_x >= HEIGHT:
                    continue

                x = mouse_x // SQ_Size
                y = mouse_y // SQ_Size

                if selected_square:
                    start_y, start_x = selected_square
                    if [y, x] in valid_moves:

                        moving_piece = game_board.board[start_y][start_x]
                        is_promotion = False

                        if moving_piece and type(moving_piece).__name__ == "Pawn":
                            if (moving_piece.color == "white" and y == 0) or (moving_piece.color == "black" and y == 7):
                                is_promotion = True

                        if is_promotion:
                            promo_choice = get_promotion_choice(screen, moving_piece.color)
                            game_board.move_piece(start_y, start_x, y, x, promotion=promo_choice)
                        else:
                            game_board.move_piece(start_y, start_x, y, x)

                        selected_square = None
                        valid_moves = []
                        game_board.check_game_over()

                        new_fen = board_to_fen(game_board)
                        move_history.append(new_fen)
                        current_history_index = len(move_history) - 1
                        viewing_history = False
                    else:
                        piece = game_board.board[y][x]
                        if piece and piece.color == game_board.who_moves:
                            selected_square = (y, x)
                            valid_moves = game_board.get_legal_moves(y, x)
                        else:
                            selected_square = None
                            valid_moves = []

                else:
                    piece = game_board.board[y][x]
                    if piece and piece.color == game_board.who_moves:
                        selected_square = (y, x)
                        valid_moves = game_board.get_legal_moves(y, x)

        if viewing_history:
            board_to_draw = parse_fen(move_history[current_history_index])
            selected_square = None
            valid_moves = []
        else:
            board_to_draw = game_board

        screen.fill((40, 40, 40))
        draw_board(screen)
        draw_selected_highlight(screen, selected_square)
        draw_check_highlight(screen, board_to_draw)
        draw_pieces(screen, board_to_draw)
        draw_hints(screen, valid_moves)
        draw_turn_indicator(screen, board_to_draw)
        draw_history_indicator(screen, viewing_history, current_history_index, len(move_history) - 1)
        draw_timers(screen, white_time, black_time)
        draw_undo_button(screen)
        draw_game_over_screen(screen, board_to_draw)
        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start game MyChess")
    parser.add_argument('--bot', action='store_true', help="Play vs AI (за черных)")
    args = parser.parse_args()
    main(play_vs_bot=args.bot)