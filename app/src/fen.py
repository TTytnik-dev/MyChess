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
    blocks = fen_string.split(" ")

    board_list = blocks[0].split('/')
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


    turns = blocks[1]

    if turns == "w":
        board.who_moves = "white"
    else:
        board.who_moves = "black"

    if len(blocks ) >= 3:
        castlings = blocks[2]

        if "Q" not in castlings:
            if  board.board[7][0] : board.board[7][0].was_moved = True
        if "K" not in castlings:
            if board.board[7][7] : board.board[7][7].was_moved = True
        if "Q" not in castlings and "K" not in castlings:
            if board.board[7][4] : board.board[7][4].was_moved = True

        if "q" not in castlings:
            if board.board[0][0] : board.board[0][0].was_moved = True
        if "k" not in castlings:
            if  board.board[0][7] : board.board[0][7].was_moved = True
        if "q" not in castlings and "k" not in castlings:
            if board.board[0][4] : board.board[0][4].was_moved = True



    if len(blocks) >= 4:
        ep = blocks[3]
        if ep != "-":
            x = ord(ep[0]) - ord('a')
            ep_y = 8 - int(ep[1])
            pawn_y = 4 if ep_y == 5 else 3
            if board.board[pawn_y][x]:
                board.en_passant_target = board.board[pawn_y][x]

    if len(blocks) >= 5:
        board.halfmove_clock = int(blocks[4])

    if len(blocks) >= 6:
        board.fullmove_number = int(blocks[5])

    return board


def board_to_fen(board):
    fen = ""
    for y in range(8):
        empty_count = 0
        for x in range(8):
            piece = board.board[y][x]
            if piece is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0

                p_type = type(piece).__name__
                char = 'n' if p_type == 'Knight' else p_type[0].lower()

                if piece.color == "white":
                    fen += char.upper()
                else:
                    fen += char.lower()

        if empty_count > 0:
            fen += str(empty_count)
        if y < 7:
            fen += "/"

    fen += " " + ("w" if board.who_moves == "white" else "b")

    castling = ""
    wk = board.board[7][4]
    if wk and type(wk).__name__ == 'King' and wk.color == 'white' and not getattr(wk, 'was_moved', False):
        wr_k = board.board[7][7]
        wr_q = board.board[7][0]
        if wr_k and type(wr_k).__name__ == 'Rook' and wr_k.color == 'white' and not getattr(wr_k, 'was_moved', False):
            castling += "K"
        if wr_q and type(wr_q).__name__ == 'Rook' and wr_q.color == 'white' and not getattr(wr_q, 'was_moved', False):
            castling += "Q"
    bk = board.board[0][4]
    if bk and type(bk).__name__ == 'King' and bk.color == 'black' and not getattr(bk, 'was_moved', False):
        br_k = board.board[0][7]
        br_q = board.board[0][0]
        if br_k and type(br_k).__name__ == 'Rook' and br_k.color == 'black' and not getattr(br_k, 'was_moved', False):
            castling += "k"
        if br_q and type(br_q).__name__ == 'Rook' and br_q.color == 'black' and not getattr(br_q, 'was_moved', False):
            castling += "q"

    if castling == "":
        castling = "-"
    fen += " " + castling

    ep_str = "-"
    if board.en_passant_target is not None:
        ep_pawn = board.en_passant_target
        file_char = chr(ord('a') + ep_pawn.x)
        if ep_pawn.color == "white" and ep_pawn.y == 4:
            ep_str = f"{file_char}3"
        elif ep_pawn.color == "black" and ep_pawn.y == 3:
            ep_str = f"{file_char}6"

    fen += " " + ep_str

    fen += f" {board.halfmove_clock} {board.fullmove_number}"

    return fen

