import re
import chess.pgn
import chess.engine
import chess.polyglot as polyglot

MOVES = "Moves"
EVALS = "Evals"
ENGINE_EVALS = "EngineEvals"
COMMENTS = "Comments"
WHITE_CENTER = "WhiteCenter"
BLACK_CENTER = "BlackCenter"
WHITE_DIAGONAL = "WhiteDiag"
BLACK_DIAGONAL = "BlackDiag"
WHITE_PINS = "WhitePins"
BLACK_PINS = "BlackPins"
ZOBRIST_HASH = "ZobristHash"
BOARD_2D = "Board2D"


def get_move(node):
    next_node = node.variation(0)
    return node.board().san(next_node.move)


def get_move_acpl(node):
    next_node = node.variation(0)
    acpl_match = re.match("\[\%eval (.*?)\]", next_node.comment)
    return acpl_match.group(1) if acpl_match is not None else 'X'


def get_move_comment(node):
    next_node = node.variation(0)
    nags = next_node.nags
    return -1 if len(nags) == 0 else list(nags)[0]


def get_center_control(node):
    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    return get_number_of_attackers(node.board(), center_squares)


def get_diagonal_control(node):
    main_diagonal = [chess.A8, chess.B7, chess.C6, chess.D5, chess.E4, chess.F3, chess.G2, chess.H1]
    oppo_diagonal = [chess.A1, chess.B2, chess.C3, chess.D4, chess.E5, chess.F6, chess.G7, chess.H8]
    diagonal_squares = main_diagonal + oppo_diagonal
    return get_number_of_attackers(node.board(), diagonal_squares)


def get_engine_eval(engine, depth, time, node):
    board = node.board()
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    # info = engine.analyse(board, chess.engine.Limit(time=time, depth=depth))
    return str(info.score)


def get_zobrist_hash(node):
    return polyglot.zobrist_hash(node.board())


def get_number_of_attackers(board, squares):
    white = 0
    black = 0
    for square in squares:
        white += len(board.attackers(chess.WHITE, square))
        black += len(board.attackers(chess.BLACK, square))

    return white, black


def get_number_of_pins(node):
    board = node.board()
    return get_number_of_pins_for_color(board, chess.WHITE), get_number_of_pins_for_color(board, chess.BLACK)


def get_number_of_pins_for_color(board, color):
    squares = get_significant_pieces_squares(board, color)
    count = 0
    for square in squares:
        if board.is_pinned(color, square):
            count += 1
    return count


def get_significant_pieces_squares(board, color):
    knight_squares = board.pieces(chess.KNIGHT, color)
    bishop_squares = board.pieces(chess.BISHOP, color)
    rook_squares = board.pieces(chess.ROOK, color)
    queen_squares = board.pieces(chess.QUEEN, color)
    return knight_squares.union(bishop_squares).union(rook_squares).union(queen_squares)


def get_board_2d(node):
    board = node.board()
    result = []
    builder = []

    for square in chess.SQUARES_180:
        piece = board.piece_at(square)

        if piece:
            builder.append(piece.piece_type if piece.color else -piece.piece_type)
        else:
            builder.append(0)

        if chess.BB_SQUARES[square] & chess.BB_FILE_H:
            result.append(builder.copy())
            builder.clear()

    return result
