class Piece:
    def __init__(self, y, x, color):
        self.x = x
        self.y = y
        self.color = color

    def sliding_moves(self, board, directions):
        start_x = self.x
        start_y = self.y

        valid_moves = []

        for dy, dx in directions:
            curr_x = start_x + dx
            curr_y = start_y + dy
            while 0 <= curr_x <= 7 and 0 <= curr_y <= 7 and board.board[curr_y][curr_x] is None:
                valid_moves.append([curr_y, curr_x])
                curr_x = curr_x + dx
                curr_y = curr_y + dy
            if not 0 <= curr_x <= 7 or not 0 <= curr_y <= 7:
                continue

            if board.board[curr_y][curr_x].color != self.color:
                valid_moves.append([curr_y, curr_x])
            else:
                continue

        return valid_moves

    def step_moves(self, board, directions):
        valid_moves = []
        for dy, dx in directions:
            new_x = dx + self.x
            new_y = dy + self.y
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if board.board[new_y][new_x] is None:
                    valid_moves.append([new_y, new_x])
                elif board.board[new_y][new_x].color != self.color:
                    valid_moves.append([new_y, new_x])

        return valid_moves


class Pawn(Piece):
    def get_valid_moves(self, board):
        valid_moves = []
        if self.color == "black":
            step_forward = self.y + 1
            if 2 <= step_forward <= 7 and board.board[step_forward][self.x] is None:
                valid_moves.append([step_forward, self.x])
            diagonal_steps = [(1, 1), (1, -1)]
            for dy, dx in diagonal_steps:
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x <= 7 and 2 <= new_y <= 7 and board.board[new_y][new_x] is not None and board.board[new_y][
                    new_x].color != self.color:
                    valid_moves.append([new_y, new_x])
            if self.y == 1 and board.board[self.y + 2][self.x] is None and board.board[step_forward][self.x] is None:
                valid_moves.append([self.y + 2, self.x])
        else:
            step_forward = self.y - 1
            if 0 <= step_forward <= 5 and board.board[step_forward][self.x] is None:
                valid_moves.append([step_forward, self.x])
            diagonal_steps = [(-1, 1), (-1, -1)]
            for dy, dx in diagonal_steps:
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x <= 7 and 0 <= new_y <= 5 and board.board[new_y][new_x] is not None and board.board[new_y][
                    new_x].color != self.color:
                    valid_moves.append([new_y, new_x])
            if self.y == 6 and board.board[self.y - 2][self.x] is None and board.board[step_forward][self.x] is None:
                valid_moves.append([self.y - 2, self.x])

        return valid_moves


class King(Piece):
    directions = [(1, 1), (1, -1), (1, 0), (-1, 1), (0, 1), (0, -1), (-1, 0), (-1, -1)]

    def get_valid_moves(self, board):
        return self.step_moves(board, self.directions)


class Queen(Piece):
    def get_valid_moves(self, board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.sliding_moves(board, directions)


class Bishop(Piece):
    def get_valid_moves(self, board):
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        return self.sliding_moves(board, directions)


class Rook(Piece):
    def get_valid_moves(self, board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self.sliding_moves(board, directions)


class Knight(Piece):
    def get_valid_moves(self, board):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        return self.step_moves(board, directions)
