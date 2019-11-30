import os
import time

from mpi4py import MPI

start_time = time.time()

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print("This is node {}".format(rank))

if rank == 0:
    print("We have {} nodes in our cluster.".format(size))
    data = [x for x in range(size)]
    print('We will be scattering files across nodes:', data)
else:
    data = None

data = comm.scatter(data, root=0)
print('rank', rank, 'has data:', data)

if rank != 0:
    command = "python pgn_to_json_csv_converter.py --files-list ./input/{}.pgn --unique-batch-identifier wowza_mpi -n 100 -b 25 --skip-games 0 -dc --engine-evals --engine-path './engine/stockfish_10_x64' --engine-eval-depth 10 --comments --center-control --diagonal-control --pins --zobrist-hash".format(
        data)
    print("Running command:", command)
    os.system(command)

print("Completed in {:.2f}s for rank {}:".format(time.time() - start_time, rank))
