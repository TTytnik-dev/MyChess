class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def put_piece(self, y, x, piece):
        self.board[y][x] = piece

    def clear_square(self, y, x):
        self.board[y][x] = None

    WhoMoves = "white"
