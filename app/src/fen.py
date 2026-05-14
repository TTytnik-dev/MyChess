from app.src import pieces

def validate_fen(fen_string):
    blocks = fen_string.split(" ")

    if not 2 <= len(blocks) <= 6:
        raise Exception("Invalid FEN string")

    parts = blocks[0].split('/')
    if len(parts) != 8:
        raise ValueError("A small number of rows on the board")

    board_block = blocks[0]

    if board_block.count("k") != 1:
        raise Exception ("black king must be 1")
    if board_block.count("K") != 1:
        raise Exception ("white king must be 1")
    if board_block.count("p") > 8:
        raise Exception ("black pawns cant be more then 8")
    if board_block.count("P") > 8:
        raise Exception ("white pawns cant be more than 8")

    for row in parts:
        count = 0
        for pos in row:
            if pos.isalpha() and pos in "pnbrqkPNBRQK":
                count += 1
            elif pos.isdigit() and 1 <= int(pos) <= 8:
                count += int(pos)
            else:
                raise Exception("Invalid FEN string")
        if count != 8:
            raise Exception("Invalid FEN string")

    if blocks[1] != "w" and blocks[1] != "b":
        raise Exception("Invalid FEN string")

    if len(blocks) >= 3:
        third = blocks[2]
        if third == '-':
            pass
        else:
            if len(third) < 1 or len(third) > 4:
                raise Exception("Invalid FEN string")

            for x in third:
                if x not in "kqKQ":
                    raise Exception("Invalid FEN string")
            if third.count("k") > 1 or third.count("q") > 1 or third.count("K") > 1 or third.count("Q") > 1:
                raise Exception("Invalid FEN string")

    if len(blocks) >= 4:
        four = blocks[3]
        if four == '-':
            pass
        else:
            if len(four) != 2:
                raise Exception("Invalid FEN string")
            if four[0] not in "abcdefgh" or four[1] not in "36":
                raise Exception("Invalid FEN string")

    if len(blocks) >= 5:
        if blocks[4].isdigit() and int(blocks[4]) >= 0:
            pass
        else:
            raise Exception("Invalid FEN string")

        if len(blocks) >= 6:
            if blocks[5].isdigit() and int(blocks[5]) > 0:
                pass
            else:
                raise Exception("Invalid FEN string")


def parse_fen(fen_string):
    from app.src.board import Board
    validate_fen(fen_string)
    piece_mapping = {
        'p': pieces.Pawn,
        'n': pieces.Knight,
        'b': pieces.Bishop,
        'r': pieces.Rook,
        'q': pieces.Queen,
        'k': pieces.King
    }

    board = Board()

    board_list = fen_string.split(" ")[0].split('/')
    for y, row in enumerate(board_list):
        board_x = 0
        for x in range(len(row)):
            if row[x].isalpha():
                if row[x].islower():
                    board.put_piece(y, board_x, piece_mapping[row[x]](y, board_x, "black"))
                    board_x += 1
                else:
                    place = row[x].lower()
                    board.put_piece(y, board_x, piece_mapping[place](y, board_x, "white"))
                    board_x += 1
            else:
                board_x += int(row[x])

    turns = fen_string.split(" ")[1]

    if turns == "w":
        board.WhoMoves = "white"
    else:
        board.WhoMoves = "black"

    return board
