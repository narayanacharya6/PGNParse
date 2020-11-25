### WHY THIS README?

This could have easily been a script but why did I choose to have this as a readme?
Be careful after each step. This is a shared cluster. You would not want to affect other nodes because you ran a stupid 
script! Also calling module load one after the other seems to be flaky and does not load everything!

### Load required modules
```
module load shared
module load git
module load anaconda/3
module load slurm
module load mvapich2/gcc7.1/64/2.2rc1
```

### Go to working directory!
```
cd DSF-Project/PGNParsing/PGNParse/
```

### Get the correct version for mpi4py.
#### The one there is just messed up!
```
source activate pgn-parse
pip install --user -r requirements.txt
```

### Change permission on the stockfish engine!
```
chmod 700 ./engine/stockfish_10_x64
```

### Go to a compute node of choice for interactive work. Use something like...
```
srun -N 8 -n 28 -p debug-28core --pty bash
```

### To submit a long running batch
### Tweak the mpi_parser_slurm.sh accordingly then submit using
```
sbatch mpi_parser_slurm.sh
```

### Command for running mpi parser
### Check arguments in mpi_parser before running this! I know this should be better but we are running out of time!!!
```
mpirun -n 2 python mpi_parser.py 2> error.out 1> log.out
```
