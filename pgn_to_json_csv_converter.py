import sys
import json
import csv
import chess.pgn
import re
import sys
import time

files = sys.argv[1].split(',')
print('Gathering from files:', files)
mode = sys.argv[2]
default_n = 1000
default_b = 100
dump = False
if sys.argv[3] != None:
    default_n = int(sys.argv[3])
if sys.argv[4] != None:
    default_b = int(sys.argv[4])
if sys.argv[5] != None:
    dump = sys.argv[5].lower() == 'true'

games = []
games_to_get_per_file = default_n
batch_size = default_b
start_time = time.time()
failed_games = 0

for file_name in files:
    x = 'lichess_db_standard_rated_{}.pgn'.format(file_name)
    try:
        pgn = open(x)
    except:
        print("File not found: {}!".format(x))
        raise SystemExit

    print('Starting with file:', pgn)
    games_from_file = []
    batch_start_time = time.time()

    node = chess.pgn.read_game(pgn)
    while node != None and len(games_from_file) < games_to_get_per_file:
        try:
            data = {}
            header_keys = [n for n in node.headers]

            for header_key in header_keys:
                data[header_key] = node.headers[header_key]

            data["Moves"] = []
            # Eval not available in many-a-games (almost 85%)!
            # Add only if really required.
            # Will save comp time as regex matching no longer required!
            # data["Evals"] = []
            data["Comments"] = []
            data["WhiteCenter"] = []
            data["BlackCenter"] = []
            # Skipping diagonal as it takes a lot of time to compute!
            # data["WhiteDiag"] = []
            # data["BlackDiag"] = []

            while node.variations:
                next_node = node.variation(0)
                # acpl_match = re.match("\[\%eval (.*?)\]", next_node.comment)
                nags = next_node.nags
                data["Moves"].append(node.board().san(next_node.move))
                # data["Evals"].append(acpl_match.group(1) if acpl_match != None else "X")
                data["Comments"].append(-1 if len(nags) == 0 else list(nags)[0])

                # Center control
                center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
                white_center = 0
                black_center = 0
                for center_square in center_squares:
                    white_center += len(node.board().attackers(chess.WHITE, center_square))
                    black_center += len(node.board().attackers(chess.BLACK, center_square))

                # Diagonal Control
                # main_diagonal = [chess.A8, chess.B7, chess.C6, chess.D5, chess.E4, chess.F3, chess.G2, chess.H1]
                # oppo_diagonal = [chess.A1, chess.B2, chess.C3, chess.D4, chess.E5, chess.F6, chess.G7, chess.H8]
                # diagonal_squares = main_diagonal + oppo_diagonal
                # # print(diagonal_squares)
                # white_diagonal = 0
                # black_diagonal = 0
                # for diag_square in diagonal_squares:
                #     white_diagonal += len(node.board().attackers(chess.WHITE, diag_square))
                #     black_diagonal += len(node.board().attackers(chess.BLACK, diag_square))

                data["WhiteCenter"].append(white_center)
                data["BlackCenter"].append(black_center)
                # data["WhiteDiag"].append(white_diagonal)
                # data["BlackDiag"].append(black_diagonal)
                # print(white_center, black_center, white_diagonal, black_diagonal)
                # print(node.board())
                node = next_node

            games_from_file.append(data)

            if len(games_from_file) % default_b == 0:
                now_time = time.time()
                print("Processed games: {:>5} | Process time: {:8.2f} | Batch time: {:5.2f}"
                      .format(len(games_from_file), now_time - start_time, now_time - batch_start_time))
                batch_start_time = time.time()

            node = chess.pgn.read_game(pgn)
        except:
            # Do nothing if single parsing fails!
            failed_games += 1

    print('{} games retrieved from file {}'.format(len(games_from_file), file_name))
    games.extend(games_from_file)

    try:
        pgn.close()
    except Exception as inst:
        print('Something went wrong while closing pgn file!')
        print(inst)

print('Failed to process games: {}'.format(failed_games))

if dump:
    print("All files read! Dumping to json and CSV!")
    file_name = 'data_{}'.format(int(round(time.time() * 1000)))

    try:
        json_file = open(file_name + '.json', mode)
        json.dump(games, json_file)
        json_file.close()
    except Exception as inst:
        print('Something went wrong with JSON dump!')
        print(inst)

    try:
        csv_file = open(file_name + '.csv', mode)
        keys = games[0].keys()
        # Extrasaction ignore keys not in dict
        # Think again if we need this, example missing key is 'BlackTitle "LM"'
        dict_writer = csv.DictWriter(csv_file, keys, extrasaction='ignore')
        dict_writer.writeheader()
        dict_writer.writerows(games)
        csv_file.close()
    except Exception as inst:
        print('Something went wrong with CSV dump!')
        print(inst)
else:
    print('Not dumping games to JSON and CSV')

print('Done! Processed games: ', len(games))
