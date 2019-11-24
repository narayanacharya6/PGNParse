import os
import sys
import time
import argparse

# External Project Imports
import chess.pgn
import chess.engine

# Project Import
import arg_checker
import features
import dumper

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files-list', nargs='+', default=[])
parser.add_argument('-n', '--number-of-games', default=0)
parser.add_argument('-b', '--batch-of-games', default=0)
parser.add_argument('-dj', '--dump-json', action='store_true', default=False)
parser.add_argument('-dc', '--dump-csv', action='store_true', default=False)
parser.add_argument('-o', '--output-dir', type=arg_checker.dir_path, default='./output/')
parser.add_argument('--moves', action='store_true', default=True)
parser.add_argument('--evals', action='store_true', default=False)
parser.add_argument('--engine-evals', action='store_true', default=False)
parser.add_argument('--engine-path', default='./engine/stockfish_10_x64.exe')
parser.add_argument('--engine-eval-depth', default=20)
parser.add_argument('--engine-eval-time', default=0.1)
parser.add_argument('--comments', action='store_true', default=True)
parser.add_argument('--center-control', action='store_true', default=False)
parser.add_argument('--diagonal-control', action='store_true', default=False)
args = parser.parse_args()

print('------------------------------')
print('Gathering from files?:', args.files_list)
print('Number of games to parse per file?:', args.number_of_games)
print('Print every how many number of games?:', args.batch_of_games)
print('Dumping to JSON?:', args.dump_json)
print('Dumping to CSV?:', args.dump_csv)
print('Dumping to JSON and CSV where?:', args.output_dir)
print('------------------------------')
print('Getting moves?:', args.moves)
print('Getting evals?:', args.evals)
print('Getting engine evals?:', args.engine_evals)
print('Getting comments?:', args.comments)
print('Getting center control?:', args.center_control)
print('Getting diagonal control?:', args.diagonal_control)
print()

games = []
games_to_get_per_file = int(args.number_of_games)
batch_size = int(args.batch_of_games)
start_time = time.time()
failed_games = 0

for file_name in args.files_list:
    try:
        pgn = open(file_name)
    except Exception as e:
        print("File not found: {}!".format(file_name))
        raise SystemExit

    print('------------------------------')
    print('Starting with file:', pgn.name)
    games_from_file = []
    batch_start_time = time.time()

    stockfish_engine = chess.engine.SimpleEngine.popen_uci(args.engine_path)
    engine_eval_depth = int(args.engine_eval_depth)
    engine_eval_time = float(args.engine_eval_time)
    node = chess.pgn.read_game(pgn)
    while node is not None and len(games_from_file) < games_to_get_per_file:
        try:
            data = {}
            header_keys = [n for n in node.headers]

            for header_key in header_keys:
                data[header_key] = node.headers[header_key]

            if args.moves:
                data[features.MOVES] = []

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

            while node.variations:
                next_node = node.variation(0)
                nags = next_node.nags

                # Moves
                if args.moves:
                    data[features.MOVES].append(features.get_move(node))

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

    print('{} games retrieved from file {}'.format(len(games_from_file), file_name))
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

print('Failed to process games: {}'.format(failed_games))

print()
print('------------------------------')
if args.dump_json or args.dump_csv:
    print("All files read! Dumping to JSON and/or CSV!")
    timestamp = str(round(time.time() * 1000))
    output_dir = os.path.join(args.output_dir, timestamp)
    file_name = 'data'

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
