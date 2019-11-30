### Load required modules
module load shared
module load git
module load anaconda/3
module load slurm
module load mvapich2/gcc7.1/64/2.2rc1

### Get the correct version for mpi4py.
#### The one there is just messed up!
source activate pgn-parse
pip install --user -r requirements.txt

### Command for running mpi parser
### Check arguments in mpi_parser before running this! I know this should be better but we are running out of time!!!
mpirun -n 2 python mpi_parser.py 2> error.out 1> log.out

