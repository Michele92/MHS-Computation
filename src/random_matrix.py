"""Permette di generare una matrice casuale avente le dimensioni specificate e calcolarne l'espressione"""

import re
import sys
import time

import numpy as np

from utils import *

MATRIX_DIR = 'matrix/'
MHS_DIR = 'mhs'
ONE_PROBABILITY = 0.5
PROBABILITIES = [1 - ONE_PROBABILITY, ONE_PROBABILITY]

if __name__ == '__main__':
    file_name = sys.argv[1]
    nrows, ncols = int(sys.argv[2]), int(sys.argv[3])
    with open(MATRIX_DIR + file_name + '.matrix', mode='w') as f:
        for _ in range(nrows):
            f.write(' '.join([str(np.random.choice([0, 1], p=PROBABILITIES)) for i in range(ncols)]) + ' -\n')
    f.close()
    with open(MATRIX_DIR + file_name + '.matrix') as f:
        lines = f.readlines()
        rows = []
        for line in lines:
            if not line.startswith(';'):
                rows.append(line[:-2].replace(' ', ''))
    f.close()
    matrix = Matrix(rows)
    mhs_dir = create_dir(MHS_DIR)
    start = time.clock()
    expr = compute_mhs(matrix)
    elapsed_time = time.clock() - start
    found_solutions = eval(re.sub(r'[0-9]+', '1', str(expr)))
    print 'Found ' + str(found_solutions) + ' solutions in ' + str(round(elapsed_time, 3)) + ' s'
    with open(mhs_dir + file_name + '.mhs', mode='w') as f:
        f.write(str(expr))
    f.close()
