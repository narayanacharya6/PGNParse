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
ZOBRIST_HASH = "ZobristHash"


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
    info = engine.analyse(board, chess.engine.Limit(time=time, depth=depth))
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
