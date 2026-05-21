from app.src.pieces import Piece, King

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

        if [end_y, end_x] not in self.get_legal_moves(piece.y, piece.x):
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

    def is_in_check(self, color):
        king_y, king_x = None, None
        for y in range(8):
            for x in range(8):
                if isinstance(self.board[y][x], King) and self.board[y][x].color == color:
                    king_y = y
                    king_x = x
                    break

        if king_y is None:
            raise Exception("King not found")

        for y in range(8):
            for x in range(8):
                piece : Piece | None = self.board[y][x]
                if piece is not None and piece.color != color:
                    if [king_y, king_x] in piece.get_valid_moves(self):
                        return True

        return False

    def get_legal_moves(self, piece_y ,piece_x ):
        legal_moves = []

        if self.board[piece_y][piece_x] is  None:
            return legal_moves

        piece = self.board[piece_y][piece_x]
        for [y , x] in piece.get_valid_moves(self):

            old_x = piece.x
            old_y = piece.y
            piece_type = self.board[y][x]

            self.board[old_y][old_x] = None
            self.board[y][x] = piece

            piece.x = x
            piece.y = y

            if not self.is_in_check(piece.color):
                    legal_moves.append([y, x])

            self.board[old_y][old_x] = piece
            self.board[y][x] = piece_type
            piece.x = old_x
            piece.y = old_y

        return legal_moves
