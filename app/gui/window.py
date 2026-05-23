import pygame
import sys
import os
from app.src.fen import parse_fen
from app.src.pieces import Pawn

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




def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    load_images()

    game_board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(screen)
        draw_pieces(screen, game_board)
        pygame.display.flip()


if __name__ == "__main__":
    main()