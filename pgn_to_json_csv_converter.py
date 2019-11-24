import os
import sys
import json
import csv
import chess.pgn
import re
import sys
import time
import argparse

import arg_checker

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files-list', nargs='+', default=[])
parser.add_argument('-n', '--number-of-games', default=0)
parser.add_argument('-b', '--batch-of-games', default=0)
parser.add_argument('-dj', '--dump-json', action='store_true', default=False)
parser.add_argument('-dc', '--dump-csv', action='store_true', default=False)
parser.add_argument('-o', '--output-dir', type=arg_checker.dir_path, default='./output/')
parser.add_argument('--moves', action='store_true', default=True)
parser.add_argument('--evals', action='store_false', default=False)
parser.add_argument('--comments', action='store_true', default=True)
parser.add_argument('--center-control', action='store_false', default=False)
parser.add_argument('--diagonal-control', action='store_false', default=False)
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
print('Getting comments?:', args.comments)
print('Getting center control?:', args.center_control)
print('Getting diagonal_control?:', args.diagonal_control)
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

    node = chess.pgn.read_game(pgn)
    while node is not None and len(games_from_file) < games_to_get_per_file:
        try:
            data = {}
            header_keys = [n for n in node.headers]

            for header_key in header_keys:
                data[header_key] = node.headers[header_key]

            if args.moves:
                data["Moves"] = []

            # Eval not available in many-a-games (almost 85%)!
            # Add only if really required.
            # Will save comp time as regex matching no longer required!
            if args.evals:
                data["Evals"] = []

            if args.comments:
                data["Comments"] = []

            if args.center_control:
                data["WhiteCenter"] = []
                data["BlackCenter"] = []

            if args.diagonal_control:
                data["WhiteDiag"] = []
                data["BlackDiag"] = []

            while node.variations:
                next_node = node.variation(0)
                nags = next_node.nags

                # Moves
                if args.moves:
                    data["Moves"].append(node.board().san(next_node.move))

                # Evals
                if args.evals:
                    acpl_match = re.match("\[\%eval (.*?)\]", next_node.comment)
                    data["Evals"].append(acpl_match.group(1) if acpl_match is not None else "X")

                # Comments
                if args.comments:
                    data["Comments"].append(-1 if len(nags) == 0 else list(nags)[0])

                # Center control
                if args.center_control:
                    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
                    white_center = 0
                    black_center = 0
                    for center_square in center_squares:
                        white_center += len(node.board().attackers(chess.WHITE, center_square))
                        black_center += len(node.board().attackers(chess.BLACK, center_square))

                    data["WhiteCenter"].append(white_center)
                    data["BlackCenter"].append(black_center)

                # Diagonal Control
                if args.diagonal_control:
                    main_diagonal = [chess.A8, chess.B7, chess.C6, chess.D5, chess.E4, chess.F3, chess.G2, chess.H1]
                    oppo_diagonal = [chess.A1, chess.B2, chess.C3, chess.D4, chess.E5, chess.F6, chess.G7, chess.H8]
                    diagonal_squares = main_diagonal + oppo_diagonal
                    # print(diagonal_squares)
                    white_diagonal = 0
                    black_diagonal = 0
                    for diag_square in diagonal_squares:
                        white_diagonal += len(node.board().attackers(chess.WHITE, diag_square))
                        black_diagonal += len(node.board().attackers(chess.BLACK, diag_square))

                    data["WhiteDiag"].append(white_diagonal)
                    data["BlackDiag"].append(black_diagonal)

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

print('Failed to process games: {}'.format(failed_games))

print()
print('------------------------------')
if args.dump_json or args.dump_csv:
    print("All files read! Dumping to JSON and/or CSV!")
    timestamp = str(round(time.time() * 1000))
    output_dir = os.path.join(args.output_dir, timestamp)
    file_name = 'data'

    if args.dump_json:
        try:
            json_file_path = os.path.join(output_dir, file_name + '.json')
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
            json_file = open(json_file_path, 'w')

            json.dump(games, json_file)
            json_file.close()
            print('JSON dump complete:!', json_file.name)
        except Exception as inst:
            print('Something went wrong with JSON dump!', inst)
    else:
        print('Not dumping games to JSON')

    if args.dump_csv:
        try:
            csv_file_path = os.path.join(output_dir, file_name + '.csv')
            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
            csv_file = open(csv_file_path, 'w')

            keys = games[0].keys()
            # Extrasaction ignore keys not in dict
            # Think again if we need this, example missing key is 'BlackTitle "LM"'
            dict_writer = csv.DictWriter(csv_file, keys, extrasaction='ignore')
            dict_writer.writeheader()
            dict_writer.writerows(games)
            csv_file.close()
            print('CSV dump complete:!', csv_file.name)
        except Exception as inst:
            print('Something went wrong with CSV dump!', inst)
    else:
        print('Not dumping games to CSV')

print()
print('------------------------------')
print('Done! Processed games: ', len(games))
