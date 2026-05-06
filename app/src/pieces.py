class Piece:
    def __init__(self, y, x, color):
        self.x = x
        self.y = y
        self.color = color
        self.history = 0

class Pawn(Piece):
    pass

class King(Piece):
    pass

class Queen(Piece):
    pass

class Bishop(Piece):
    pass

class Rook(Piece):
    pass

class Knight(Piece):
    pass