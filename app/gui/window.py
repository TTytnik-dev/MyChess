import pygame
import sys
import os
from app.src.pieces import King
from app.src.fen import parse_fen, board_to_fen
import argparse
import random
import time
import subprocess
from stockfish import Stockfish

IMAGES = {}

HEIGHT = 800
UI_WIDTH = 250
WIDTH = 800 + UI_WIDTH
SQ_Size = 800 // 8
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

def draw_board(screen, flipped):
    for y in range(8):
        for x in range(8):
            render_y, render_x = (7 - y, 7 - x) if flipped else (y, x)
            if ((y + x) % 2) == 0:
                pygame.draw.rect(screen, LIGHT, pygame.Rect(render_x * SQ_Size, render_y * SQ_Size, SQ_Size, SQ_Size))
            else:
                pygame.draw.rect(screen, DARK, pygame.Rect(render_x * SQ_Size, render_y * SQ_Size, SQ_Size, SQ_Size))


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']

    for piece in pieces:
        path = os.path.join("assets", "images", f"{piece}.png")

        try:
            image = pygame.image.load(path)
            IMAGES[piece] = pygame.transform.scale(image, (SQ_Size, SQ_Size))
        except Exception as e:
            print(f"Cant add {path}. Error: {e}")

def draw_pieces(screen, game_board, flipped):
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

                if flipped :
                    render_y, render_x = (7 - y, 7 - x)
                else:
                    render_y, render_x = (y, x)

                screen.blit(
                    IMAGES[key],
                    pygame.Rect(render_x * SQ_Size, render_y * SQ_Size, SQ_Size, SQ_Size)
                )


def draw_hints(screen, valid_moves, flipped):
    for move in valid_moves:
        y, x = move

        if flipped:
            render_y, render_x = (7 - y, 7 - x)
        else:
            render_y, render_x = (y, x)

        center_x = render_x * SQ_Size + SQ_Size // 2
        center_y = render_y * SQ_Size + SQ_Size // 2

        pygame.draw.circle(screen, (169, 169, 169), (center_x, center_y), SQ_Size // 10)



def draw_selected_highlight(screen, selected_square, flipped):
    if selected_square is not None:
        y, x = selected_square

        if flipped:
            render_y, render_x = (7 - y, 7 - x)
        else:
            render_y, render_x = (y, x)

        highlight_color = (255, 226, 142)

        pygame.draw.rect(
            screen,
            highlight_color,
            pygame.Rect(render_x * SQ_Size, render_y * SQ_Size, SQ_Size, SQ_Size)
        )

def draw_hover_highlight(screen, hover_y, hover_x, flipped):
    if hover_y is not None and hover_x is not None:
        if flipped:
            render_y, render_x = (7 - hover_y, 7 - hover_x)
        else:
            render_y, render_x =  (hover_y, hover_x)

        rect = pygame.Rect(render_x * SQ_Size, render_y * SQ_Size, SQ_Size, SQ_Size)

        pygame.draw.rect(screen, (255, 255, 255), rect, 4)

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

def draw_check_highlight(screen, board, flipped):
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
        render_y, render_x = (7 - king_y, 7 - king_x) if flipped else (king_y, king_x)
        red_square_rect = pygame.Rect(
            render_x * SQ_Size,
            render_y * SQ_Size,
            SQ_Size,
            SQ_Size
        )
        pygame.draw.rect(screen, (255, 0, 0), red_square_rect)

def draw_load_fen_button(screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20, bold=True)

    button_rect = pygame.Rect(HEIGHT + 20, 340, 160, 40)

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        color = (100, 100, 100)
    else:
        color = (70, 70, 70)
    pygame.draw.rect(screen, color, button_rect, border_radius=5)

    text_surface = font.render("LOAD FEN", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect

def draw_flip_board_button(screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20, bold=True)

    button_rect = pygame.Rect(HEIGHT + 20, 400, 160, 40)

    mouse_pos = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse_pos):
        color = (100, 100, 100)
    else:
        color = (70, 70, 70)

    pygame.draw.rect(screen, color, button_rect, border_radius=5)

    text_surface = font.render("FLIP BOARD", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

    return button_rect

def draw_fen_input_overlay(screen, text, error=False, selected=False):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    pygame.font.init()
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    input_font = pygame.font.SysFont('Courier', 20)
    error_font = pygame.font.SysFont('Arial', 24, bold=True)

    title = title_font.render("Enter FEN String (ENTER to load, ESC to cancel):", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))

    input_box = pygame.Rect(50, HEIGHT // 2 - 20, WIDTH - 100, 50)
    pygame.draw.rect(screen, (50, 50, 50), input_box)
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

    if selected and text:
        text_width, text_height = input_font.size(text)
        highlight_rect = pygame.Rect(input_box.x + 10, input_box.y + 12, text_width, text_height)
        pygame.draw.rect(screen, (0, 120, 215), highlight_rect)

    cursor = "|" if int(time.time() * 2) % 2 == 0 and not selected else ""

    txt_surface = input_font.render(text + cursor, True, (255, 255, 255))
    screen.blit(txt_surface, (input_box.x + 10, input_box.y + 12))

    if error:
        err_txt = error_font.render("Invalid FEN! Please check the syntax.", True, (255, 80, 80))
        screen.blit(err_txt, (WIDTH // 2 - err_txt.get_width() // 2, HEIGHT // 2 + 50))


def draw_coordinates(screen, flipped):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 14, bold=True)

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

    if flipped:
        files = files[::-1]
        ranks = ranks[::-1]

    for i in range(8):
        file_text = font.render(files[i], True, (100, 100, 100))
        screen.blit(file_text, (i * SQ_Size + 5, 780))
        rank_text = font.render(ranks[i], True, (100, 100, 100))
        screen.blit(rank_text, (5, (7 - i) * SQ_Size + 5))

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


def main(play_vs_bot=False, bot_color="black"):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.key.set_repeat(400, 50)

    try:
        pygame.scrap.init()
    except Exception as e:
        print(f"Clipboard not available: {e}")

    load_images()

    stockfish_engine = None
    try:
        stockfish_engine = Stockfish("stockfish")
        #0 - new_player, 10 - master candidate , 20 - monster
        stockfish_engine.set_skill_level(8)
        print("Stockfish engine loaded successfully! Skill level: 8")
    except Exception as e:
        print(f"Stockfish not found, falling back to random bot. Error: {e}")

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
    inputting_fen = False
    fen_text = ""
    fen_error = False
    fen_selected = False

    if play_vs_bot and bot_color == "white":
        board_flipped = True
    else:
        board_flipped = False

    while True:
        if play_vs_bot and game_board.who_moves == bot_color and not game_board.game_over_status and not viewing_history and not inputting_fen:
            pygame.time.delay(500)

            made_bot_move = False
            if stockfish_engine:
                try:
                    current_fen = board_to_fen(game_board)
                    stockfish_engine.set_fen_position(current_fen)
                    best_move = stockfish_engine.get_best_move()

                    if best_move:
                        sx = ord(best_move[0]) - ord('a')
                        sy = 8 - int(best_move[1])
                        ex = ord(best_move[2]) - ord('a')
                        ey = 8 - int(best_move[3])

                        promo = best_move[4] if len(best_move) == 5 else "q"

                        game_board.move_piece(sy, sx, ey, ex, promotion=promo)
                        made_bot_move = True
                except Exception as e:
                    print(f"Stockfish error: {e}")

            if not made_bot_move:
                all_possible_moves = []
                for y in range(8):
                    for x in range(8):
                        piece = game_board.board[y][x]
                        if piece and piece.color == bot_color:
                            moves = game_board.get_legal_moves(y, x)
                            for target_y, target_x in moves:
                                all_possible_moves.append((y, x, target_y, target_x))

                if all_possible_moves:
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

            if inputting_fen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and (event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)):
                        fen_selected = True
                        continue
                    if fen_selected and event.unicode.isprintable() and event.key not in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        fen_text = event.unicode
                        fen_selected = False
                        fen_error = False
                        continue
                    if event.key == pygame.K_RETURN:
                        try:
                            new_board = parse_fen(fen_text.strip())
                            game_board = new_board
                            move_history = [board_to_fen(game_board)]
                            current_history_index = 0
                            viewing_history = False
                            selected_square = None
                            valid_moves = []
                            white_time = 600
                            black_time = 600
                            inputting_fen = False
                            fen_error = False
                        except Exception as e:
                            fen_error = True
                    elif event.key == pygame.K_ESCAPE:
                        inputting_fen = False
                        fen_error = False
                    elif event.key == pygame.K_BACKSPACE:
                        if fen_selected:
                            fen_text = ""
                            fen_selected = False
                        else:
                            fen_text = fen_text[:-1]

                        fen_error = False
                    elif event.key == pygame.K_v and (event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META)):
                        pasted = ""
                        try:
                            if pygame.scrap.get_init():
                                for t in (pygame.SCRAP_TEXT, "UTF8_STRING", "text/plain;charset=utf-8"):
                                    try:
                                        clip = pygame.scrap.get(t)
                                        if clip:
                                            pasted = clip.decode("utf-8", errors="ignore").replace("\x00", "").strip()
                                            if pasted:
                                                break
                                    except Exception:
                                        pass
                        except Exception:
                            pass

                        if not pasted:
                            try:
                                pasted = subprocess.check_output(
                                    ["powershell.exe", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
                                    text=True
                                ).strip()
                            except Exception:
                                try:
                                    pasted = subprocess.check_output(["wl-paste", "-n"], text=True).strip()
                                except Exception:
                                    try:
                                        pasted = subprocess.check_output(
                                            ["xclip", "-selection", "clipboard", "-o"],
                                            text=True
                                        ).strip()
                                    except Exception:
                                        pasted = ""

                        if pasted:
                            if fen_selected:
                                fen_text = pasted
                                fen_selected = False
                            else:
                                fen_text += pasted
                        fen_error = False
                    else:
                        if event.unicode.isprintable():
                            if fen_selected:
                                fen_text = event.unicode
                                fen_selected = False
                            else:
                                fen_text += event.unicode

                            fen_error = False
                continue

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

                load_fen_button_rect = pygame.Rect(HEIGHT + 20, 340, 160, 40)
                if load_fen_button_rect.collidepoint((mouse_x, mouse_y)):
                    inputting_fen = True
                    fen_text = ""
                    fen_error = False
                    fen_selected = False
                    continue
                flip_button_rect = pygame.Rect(HEIGHT + 20, 400, 160, 40)

                if flip_button_rect.collidepoint((mouse_x, mouse_y)):
                    board_flipped = not board_flipped
                    continue

                if game_board.game_over_status or viewing_history:
                    continue
                if mouse_x >= HEIGHT:
                    continue

                x = mouse_x // SQ_Size
                y = mouse_y // SQ_Size

                if board_flipped:
                    x = 7 - (mouse_x // SQ_Size)
                    y = 7 - (mouse_y // SQ_Size)
                else:
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

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_y, hover_x = None, None
        if mouse_x < HEIGHT and not viewing_history and not game_board.game_over_status and not inputting_fen:
            if board_flipped:
                hover_y = 7 - (mouse_y // SQ_Size)
                hover_x = 7 - (mouse_x // SQ_Size)
            else:
                hover_y = mouse_y // SQ_Size
                hover_x = mouse_x // SQ_Size

        screen.fill((40, 40, 40))
        draw_board(screen, board_flipped)
        draw_coordinates(screen, board_flipped)
        draw_selected_highlight(screen, selected_square, board_flipped)
        draw_check_highlight(screen, board_to_draw, board_flipped)
        draw_pieces(screen, board_to_draw, board_flipped)
        draw_hover_highlight(screen, hover_y, hover_x, board_flipped)
        draw_hints(screen, valid_moves, board_flipped)

        draw_turn_indicator(screen, board_to_draw)
        draw_history_indicator(screen, viewing_history, current_history_index, len(move_history) - 1)
        draw_timers(screen, white_time, black_time)
        draw_undo_button(screen)
        draw_load_fen_button(screen)
        draw_flip_board_button(screen)

        draw_game_over_screen(screen, board_to_draw)
        if inputting_fen:
            draw_fen_input_overlay(screen, fen_text, fen_error, fen_selected)

        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start game MyChess")
    parser.add_argument('--bot', action='store_true', help="Play vs AI")
    parser.add_argument('--bot_color', type=str, choices=['white', 'black'], default='black', help="Color of the bot (white or black)")
    args = parser.parse_args()
    main(play_vs_bot=args.bot, bot_color=args.bot_color)