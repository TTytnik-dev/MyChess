import pygame
import sys
import os
from app.src.fen import parse_fen
from app.src.pieces import King

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    load_images()

    game_board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    selected_square = None
    valid_moves = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_board.game_over_status:
                    continue

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= HEIGHT:
                    continue
                x = mouse_x // SQ_Size
                y = mouse_y // SQ_Size

                if selected_square:
                    start_y, start_x = selected_square
                    if [y, x] in valid_moves:
                        game_board.move_piece(start_y, start_x, y, x)
                        selected_square = None
                        valid_moves = []
                        game_board.check_game_over()
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

        screen.fill((40, 40, 40))
        draw_board(screen)
        draw_selected_highlight(screen, selected_square)
        draw_check_highlight(screen, game_board)
        draw_pieces(screen, game_board)
        draw_hints(screen, valid_moves)
        draw_turn_indicator(screen, game_board)
        draw_game_over_screen(screen, game_board)
        pygame.display.flip()


if __name__ == "__main__":
    main()