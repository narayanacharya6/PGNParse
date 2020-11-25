#### WHY PGNParse

This project was originally built for extracting important features from a game of chess, these features can then be used
for regression/classification as part of predictive algorithms.

As part of PGNParse we look to extract these features after each step in a game of chess read from a PGN file:

"Evals": Evaluations after each move available in the PGN.

"EngineEvals": Stockfish Engine evaluations after each move.

"WhiteCenter": Number of white pieces that are attacking the 4 center squares.

"BlackCenter": Number of black pieces that are attacking the 4 center squares.

"WhiteDiag": Number of white pieces that are attacking the diagonal squares.

"BlackDiag": Number of black pieces that are attacking the diagonal squares.

"WhitePins": Number of white pieces that are pinned.

"BlackPins": Number of black pieces that are pinned.

"ZobristHash": Read more [here](https://en.wikipedia.org/wiki/Zobrist_hashing)

"Board2D": Representation of the 2D Board.

"Moves": 

"Comments": 

#### EXTRAS

Calculating these features is time consuming, because they are calculated for each move. Doing the same for close to 100k
games can take hours. In order to leverage cluster of nodes to do the same in parallel, there is provision of leveraging
multi-threading (using Python threads) and multi-processing (using MPI: Message Passing Interface). There are extra wrapper
scripts for using these as well. Look at this [file](SEAWULF_README.md) for more details for setting up your cluster.  

#### STEPS TO USE:

- Install mpi (based on your OS or your package manager)
```
brew install mpich
```

- Create a Conda environment.
```
conda create -n pgn-parse
```

- Activate the Conda environment. (Activate in each terminal you use for this project!)
```
conda activate pgn-parse
```

- Install the requirements.
```
pip install -r requirements.txt
```

- You will need a PGN file at the root of the directory for parsing.

- Check usage using:
```
python pgn_to_json_csv_converter.py --help
```

- Sample Usage:
```
python pgn_to_json_csv_converter.py --files-list sample.pgn -n 10 -b 2
```

#### TODOs:
- Add metrics.txt to output dump folder for better insight into what the dump holds.
- Add functionality to get and unzip data within the script itself if in lichess mode.
- Improve parsing performance if possible.
- Add more features for parsing. 
- Split pgn and parse separately to multi-thread possibly.
- Add more TODOs.
