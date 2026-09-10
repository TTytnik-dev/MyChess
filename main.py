from app.src import board
from app.src.fen import parse_fen
from app.src.board import Board
from app.src import pieces


def print_board(game_board):
    piece_to_char = {
        pieces.Pawn: "p",
        pieces.Knight: "n",
        pieces.Bishop: "b",
        pieces.Rook: "r",
        pieces.Queen: "q",
        pieces.King: "k",
    }

    for y in range(8):
        print(f"{8 - y} ", end=" ")
        for x in range(8):
            if game_board.board[y][x] is None:
                print(" . ", end="")
            elif game_board.board[y][x].color == "white":
                print(f" {piece_to_char[type(game_board.board[y][x])].upper()} ", end="")
            else:
                print(f" {piece_to_char[type(game_board.board[y][x])]} ", end="")
        print(f"  {8 - y}")


def moves_in_int(move):
    blocks = move.split(" ")

    start_x = ord(blocks[0][0]) - ord("a")
    start_y = 8 - int(blocks[0][1])

    end_x = ord(blocks[1][0]) - ord("a")
    end_y = 8 - int(blocks[1][1])

    return start_y, start_x, end_y, end_x


def game():
    game_board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    while True:
        print_board(game_board)
        if game_board.check_game_over():
            break

        move_str = input(f"{game_board.who_moves} make his move (e2 e4 or 'q')")

        if move_str.lower() == 'q':
            print("Game Over.")
            break

        try:
            coords = moves_in_int(move_str)
            if not game_board.move_piece(*coords):
                print("❌ Invalid move.")
        except:
            print("❌ invalid input format : e2 e4")


if __name__ == "__main__":
    game()
