#### WHY PGNParse

This project was originally built for extracting important features from a game of chess, these features can then be used
for regression/classification as part of predictive algorithms.

As part of PGNParse we look to extract features after each step in a game of chess read from a PGN file:

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

The features are then dumped into JSON/CSV files which you can then use for your predictive tasks.

Sample CSV record looks like this:
```
Event,Site,Date,Round,White,Black,Result,BlackElo,WhiteElo,Moves,Comments,WhiteCenter,BlackCenter,WhiteDiag,BlackDiag,WhitePins,BlackPins
1,kaggle.com,??,??,??,??,1/2-1/2,2411,2354,"['Nf3', 'Nf6', 'c4', 'c5', 'b3', 'g6', 'Bb2', 'Bg7', 'e3', 'O-O', 'Be2', 'b6', 'O-O', 'Bb7', 'Nc3', 'Nc6', 'Qc2', 'Rc8', 'Rac1', 'd5', 'Nxd5', 'Nxd5', 'Bxg7', 'Nf4', 'exf4', 'Kxg7', 'Qc3+', 'Kg8', 'Rcd1', 'Qd6', 'd4', 'cxd4', 'Nxd4', 'Qxf4', 'Bf3', 'Qf6', 'Nb5', 'Qxc3']","[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]","[0, 2, 2, 3, 3, 3, 3, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 6, 6, 6, 6, 7, 6, 4, 3, 5, 5, 8]","[0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 7, 6, 6, 4, 6, 5, 5, 5, 5, 5, 6, 6, 5, 5, 5, 5, 4, 4]","[8, 9, 9, 10, 10, 9, 9, 13, 13, 14, 14, 13, 13, 15, 15, 14, 14, 17, 17, 17, 17, 20, 19, 20, 20, 20, 13, 18, 19, 18, 18, 15, 14, 14, 13, 16, 16, 19]","[8, 8, 9, 9, 10, 10, 9, 9, 10, 10, 12, 12, 11, 11, 15, 15, 14, 14, 15, 15, 16, 15, 19, 13, 14, 12, 13, 13, 12, 12, 15, 15, 15, 14, 14, 14, 15, 16]","[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]","[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"
```

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
