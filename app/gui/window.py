import pygame
import sys
import os
from app.src.fen import parse_fen
from app.src.pieces import King

IMAGES = {}

WIDTH, HEIGHT = 800, 800
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
                if game_board.check_game_over():
                    continue

                mouse_x, mouse_y = pygame.mouse.get_pos()
                x = mouse_x // SQ_Size
                y = mouse_y // SQ_Size

                if selected_square:
                    start_y, start_x = selected_square
                    if [y, x] in valid_moves:
                        game_board.move_piece(start_y, start_x, y, x)
                        selected_square = None
                        valid_moves = []
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

        draw_board(screen)
        draw_check_highlight(screen, game_board)
        draw_pieces(screen, game_board)
        draw_hints(screen, valid_moves)
        pygame.display.flip()


if __name__ == "__main__":
    main()