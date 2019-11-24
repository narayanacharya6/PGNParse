#### STEPS TO USE:

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

TODOs:
- Add functionality to get and unzip data within the script itself if in lichess mode.
- Improve parsing performance if possible.
- Add more features for parsing. 
- Split pgn and parse separately to multi-thread possibly.
- Add more TODOs.
