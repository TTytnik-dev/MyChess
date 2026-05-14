class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.WhoMoves = "white"

    def put_piece(self, y, x, piece):
        self.board[y][x] = piece

    def clear_square(self, y, x):
        self.board[y][x] = None

    # def start_board(self):
    #     self.board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

