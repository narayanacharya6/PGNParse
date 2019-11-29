import os
import time
import chess
import chess.engine
import chess.pgn

import features
import dumper


def run_task(pgn=None, args=None, timestamp=None):
    if not pgn or not args or not timestamp:
        "No pgn or args or timestamp passed! How do you expect me to work?"
        return

    games = []
    games_to_get_per_file = int(args.number_of_games)
    batch_size = int(args.batch_of_games)
    start_time = time.time()
    failed_games = 0

    print('------------------------------')
    print('Starting with file:', pgn.name)
    games_from_file = []
    batch_start_time = time.time()

    stockfish_engine = chess.engine.SimpleEngine.popen_uci(args.engine_path)
    engine_eval_depth = int(args.engine_eval_depth)
    engine_eval_time = float(args.engine_eval_time)

    # Skipping games
    games_to_skip = int(args.skip_games)
    while games_to_skip > 0:
        chess.pgn.read_game(pgn)
        games_to_skip -= 1

    node = chess.pgn.read_game(pgn)
    while node is not None and len(games_from_file) < games_to_get_per_file:
        try:
            data = {}
            header_keys = [n for n in node.headers]

            for header_key in header_keys:
                data[header_key] = node.headers[header_key]

            if args.moves:
                data[features.MOVES] = []

            if args.zobrist_hash:
                data[features.ZOBRIST_HASH] = []

            if args.board_2d:
                data[features.BOARD_2D] = []

            # Eval not available in many-a-games (almost 85%)!
            # Add only if really required.
            # Will save comp time as regex matching no longer required!
            if args.evals:
                data[features.EVALS] = []

            # Stockfish engine analysis
            if args.engine_evals:
                data[features.ENGINE_EVALS] = []

            if args.comments:
                data[features.COMMENTS] = []

            # Somewhat computationally heavy!
            if args.center_control:
                data[features.WHITE_CENTER] = []
                data[features.BLACK_CENTER] = []

            # Really computationally heavy!
            if args.diagonal_control:
                data[features.WHITE_DIAGONAL] = []
                data[features.BLACK_DIAGONAL] = []

            if args.pins:
                data[features.WHITE_PINS] = []
                data[features.BLACK_PINS] = []

            while node.variations:
                next_node = node.variation(0)

                # Moves
                if args.moves:
                    data[features.MOVES].append(features.get_move(node))

                # Zobrist Hash
                if args.zobrist_hash:
                    data[features.ZOBRIST_HASH].append(features.get_zobrist_hash(node))

                # Board 2D
                if args.board_2d:
                    data[features.BOARD_2D].append(features.get_board_2d(node))

                # Evals
                if args.evals:
                    data[features.EVALS].append(features.get_move_acpl(node))

                # Engine Evals
                if args.engine_evals:
                    data[features.ENGINE_EVALS].append(features.get_engine_eval(stockfish_engine, engine_eval_depth,
                                                                                engine_eval_time, node))

                # Comments
                if args.comments:
                    data[features.COMMENTS].append(features.get_move_comment(node))

                # Center control
                if args.center_control:
                    white_center, black_center = features.get_center_control(node)
                    data[features.WHITE_CENTER].append(white_center)
                    data[features.BLACK_CENTER].append(black_center)

                # Diagonal Control
                if args.diagonal_control:
                    white_diagonal, black_diagonal = features.get_diagonal_control(node)
                    data[features.WHITE_DIAGONAL].append(white_diagonal)
                    data[features.BLACK_DIAGONAL].append(black_diagonal)

                # Pinned pieces
                if args.pins:
                    white_pins, black_pins = features.get_number_of_pins(node)
                    data[features.WHITE_PINS].append(white_pins)
                    data[features.BLACK_PINS].append(black_pins)

                node = next_node

            games_from_file.append(data)

            if len(games_from_file) % batch_size == 0:
                now_time = time.time()
                print("Processed games: {:>5} | Process time: {:8.2f} | Batch time: {:5.2f}"
                      .format(len(games_from_file), now_time - start_time, now_time - batch_start_time))
                batch_start_time = time.time()

            node = chess.pgn.read_game(pgn)
        except Exception as e:
            # Do nothing if single parsing fails just move to next game!
            node = chess.pgn.read_game(pgn)
            failed_games += 1

    print('{} games retrieved from file {}'.format(len(games_from_file), pgn.name))
    games.extend(games_from_file)

    try:
        pgn.close()
    except Exception as inst:
        print('Something went wrong while closing pgn file!')
        print(inst)

    try:
        stockfish_engine.quit()
    except Exception as inst:
        print('Something went wrong while shutting down engine!')
        print(inst)

    print()
    print('------------------------------')
    print('Failed to process games: {}'.format(failed_games))

    print()
    print('------------------------------')
    if args.dump_json or args.dump_csv:
        print("All files read! Dumping to JSON and/or CSV!")
        output_dir = os.path.join(args.output_dir, timestamp)
        file_name = '{}'.format(pgn.name)

        if args.dump_json:
            dumper.dump_json(output_dir, file_name, games)
        else:
            print('Not dumping games to JSON')

        if args.dump_csv:
            dumper.dump_csv(output_dir, file_name, games)
        else:
            print('Not dumping games to CSV')

    print()
    print('------------------------------')
    print('Done! Processed games: ', len(games))
