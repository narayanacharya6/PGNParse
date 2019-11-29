import time
import argparse
import threading

# Project Import
import arg_checker
import task

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files-list', nargs='+', default=[])
    parser.add_argument('-n', '--number-of-games', default=0)
    parser.add_argument('-b', '--batch-of-games', default=0)
    parser.add_argument('-s', '--skip-games', default=0)
    parser.add_argument('-dj', '--dump-json', action='store_true', default=False)
    parser.add_argument('-dc', '--dump-csv', action='store_true', default=False)
    parser.add_argument('-o', '--output-dir', type=arg_checker.dir_path, default='./output/')
    parser.add_argument('--moves', action='store_true', default=True)
    parser.add_argument('--zobrist-hash', action='store_true', default=False)
    parser.add_argument('--board-2d', action='store_true', default=False)
    parser.add_argument('--evals', action='store_true', default=False)
    parser.add_argument('--engine-evals', action='store_true', default=False)
    parser.add_argument('--engine-path', default='./engine/stockfish_10_x64.exe')
    parser.add_argument('--engine-eval-depth', default=20)
    parser.add_argument('--engine-eval-time', default=0.1)
    parser.add_argument('--comments', action='store_true', default=True)
    parser.add_argument('--center-control', action='store_true', default=False)
    parser.add_argument('--diagonal-control', action='store_true', default=False)
    parser.add_argument('--pins', action='store_true', default=False)
    args = parser.parse_args()

    print('------------------------------')
    print('Gathering from files?:', args.files_list)
    print('Skip games per file?:', args.skip_games)
    print('Number of games to parse per file?:', args.number_of_games)
    print('Print every how many number of games?:', args.batch_of_games)
    print('Dumping to JSON?:', args.dump_json)
    print('Dumping to CSV?:', args.dump_csv)
    print('Dumping to JSON and CSV where?:', args.output_dir)
    print('------------------------------')
    print('Getting moves?:', args.moves)
    print('Getting Zobrist hash?:', args.zobrist_hash)
    print('Getting Board 2d?:', args.board_2d)
    print('Getting evals?:', args.evals)
    print('Getting engine evals?:', args.engine_evals)
    print('Getting comments?:', args.comments)
    print('Getting center control?:', args.center_control)
    print('Getting diagonal control?:', args.diagonal_control)
    print('Getting pins?:', args.pins)
    print()

    games = []
    games_to_get_per_file = int(args.number_of_games)
    batch_size = int(args.batch_of_games)
    start_time = time.time()
    failed_games = 0

    timestamp = str(round(time.time() * 1000))
    tasks = []
    for file_name in args.files_list:
        pgn = None
        try:
            pgn = open(file_name)
        except Exception as e:
            print("File not found: {}!".format(file_name))

        t = threading.Thread(target=task.run_task, args=[pgn, args, timestamp])
        tasks.append(t)

    for t in tasks:
        t.start()

    for t in tasks:
        t.join()

    print("DONE!")
