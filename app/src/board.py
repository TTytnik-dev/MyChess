from app.src.pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.who_moves = "white"
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.game_over_status = None

    def put_piece(self, y, x, piece):
        self.board[y][x] = piece

    def clear_square(self, y, x):
        self.board[y][x] = None

    # def start_board(self):
    #     self.board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def move_piece(self, start_y, start_x, end_y, end_x, promotion="q"):

        if start_y == end_y and start_x == end_x:
            raise Exception("Invalid move")
        if (
            not 0 <= start_y <= 7
            or not 0 <= start_x <= 7
            or not 0 <= end_y <= 7
            or not 0 <= end_x <= 7
        ):
            raise Exception("Invalid coordinates")

        piece: Piece | None = self.board[start_y][start_x]
        if piece is None:
            return False

        if piece.color != self.who_moves:
            return False

        if [end_y, end_x] not in self.get_legal_moves(piece.y, piece.x):
            return False

        is_en_passant = (
            isinstance(piece, Pawn)
            and start_x != end_x
            and self.board[end_y][end_x] is None
        )

        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None

        if is_en_passant:
            self.board[start_y][end_x] = None

        if self.who_moves == "white":
            self.who_moves = "black"
        else:
            self.who_moves = "white"

        piece.x = end_x
        piece.y = end_y
        if isinstance(piece, Pawn):
            if abs(start_y - end_y) == 2:
                self.en_passant_target = self.board[end_y][end_x]
            else:
                self.en_passant_target = None
            if (piece.color == "white" and end_y == 0) or (
                piece.color == "black" and end_y == 7
            ):
                if promotion == "q":
                    self.board[end_y][end_x] = Queen(end_y, end_x, piece.color)
                elif promotion == "b":
                    self.board[end_y][end_x] = Bishop(end_y, end_x, piece.color)
                elif promotion == "n":
                    self.board[end_y][end_x] = Knight(end_y, end_x, piece.color)
                elif promotion == "r":
                    self.board[end_y][end_x] = Rook(end_y, end_x, piece.color)
        else:
            self.en_passant_target = None

        if isinstance(piece, King):
            if start_x - end_x == 2:
                if piece.color == "white":
                    rook = self.board[7][0]
                    self.board[7][3] = rook
                    self.board[7][0] = None
                    rook.x = 3
                else:
                    rook = self.board[0][0]
                    self.board[0][3] = rook
                    self.board[0][0] = None
                    rook.x = 3
            elif start_x - end_x == -2:
                if piece.color == "black":
                    rook = self.board[0][7]
                    self.board[0][5] = rook
                    self.board[0][7] = None
                    rook.x = 5
                else:
                    rook = self.board[7][7]
                    self.board[7][5] = rook
                    self.board[7][7] = None
                    rook.x = 5

        piece.was_moved = True

        return True

    def is_in_check(self, color):
        king_y, king_x = None, None
        for y in range(8):
            for x in range(8):
                if (
                    isinstance(self.board[y][x], King)
                    and self.board[y][x].color == color
                ):
                    king_y = y
                    king_x = x
                    break

        if king_y is None:
            raise Exception("King not found")

        for y in range(8):
            for x in range(8):
                piece: Piece | None = self.board[y][x]
                if piece is not None and piece.color != color:
                    if [king_y, king_x] in piece.get_valid_moves(self):
                        return True

        return False

    def get_legal_moves(self, piece_y, piece_x):
        legal_moves = []

        if self.board[piece_y][piece_x] is None:
            return legal_moves

        piece = self.board[piece_y][piece_x]
        for [y, x] in piece.get_valid_moves(self):

            old_x = piece.x
            old_y = piece.y
            piece_type = self.board[y][x]

            if isinstance(piece, King) and abs(old_x - x) == 2:
                if self.is_in_check(piece.color):
                    continue

                mid_x = (old_x + x) // 2

                self.board[old_y][old_x] = None
                self.board[old_y][mid_x] = piece
                piece.x = mid_x

                mid_safe = not self.is_in_check(piece.color)

                piece.x = old_x
                self.board[old_y][mid_x] = None
                self.board[old_y][old_x] = piece

                if not mid_safe:
                    continue

            is_en_passant = False
            captured_ep_pawn = None

            if isinstance(piece, Pawn) and x != old_x and piece_type is None:
                is_en_passant = True
                captured_ep_pawn = self.board[old_y][x]
                self.board[old_y][x] = None

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

            if is_en_passant:
                self.board[old_y][x] = captured_ep_pawn

        return legal_moves

    def check_game_over(self):
        for y in range(8):
            for x in range(8):
                square = self.board[y][x]
                if (
                    square is not None
                    and square.color == self.who_moves
                    and self.get_legal_moves(y, x)
                ):
                    return False

        if self.is_in_check(self.who_moves):
            if self.who_moves == "white":
                self.game_over_status = "black_win_checkmate"
                print("Check! Black won.")
            else:
                self.game_over_status = "white_win_checkmate"
                print("Check! White won.")
            return True
        else:
            self.game_over_status = "draw_stalemate"
            print("Stalemate! Stalemate on board.")
            return True
