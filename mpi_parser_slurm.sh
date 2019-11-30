#!/bin/bash

#SBATCH --job-name=nacharya-cse-519
#SBATCH --output=nacharya-cse-519.out
#SBATCH -p long-28core

mpirun -n 16 python mpi_parser.py