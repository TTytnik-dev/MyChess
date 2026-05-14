from app.src.pieces import Piece

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.who_moves = "white"

    def put_piece(self, y, x, piece):
        self.board[y][x] = piece

    def clear_square(self, y, x):
        self.board[y][x] = None

    # def start_board(self):
    #     self.board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def move_piece(self, start_y,start_x,end_y, end_x):

        if start_y == end_y and start_x == end_x:
            raise Exception("Invalid move")
        if not  0 <= start_y <= 7  or not  0 <= start_x <= 7 or not 0 <= end_y <= 7 or not 0 <= end_x <= 7:
            raise Exception("Invalid coordinates")

        piece : Piece | None = self.board[start_y][start_x]
        if piece  is None:
            return False

        if piece.color != self.who_moves:
            return False

        if [end_y, end_x] not in piece.get_valid_moves(self):
            return False

        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None

        if self.who_moves == "white":
            self.who_moves = "black"
        else:
            self.who_moves = "white"

        piece.x = end_x
        piece.y = end_y

        return True
