"""Contiene l'invocazione all'algoritmo che calcola l'espressione dei minimal hitting set"""

import sys
import time

from file import *
from utils import *

MATRIX_DIR = 'matrix/'
MHS_DIR = 'mhs'

if __name__ == '__main__':
    file_name = sys.argv[1]
    matrix, size = read_matrix(MATRIX_DIR + file_name + '.matrix')
    mhs_dir = create_dir(MHS_DIR)
    start = time.clock()
    expr = compute_mhs(matrix)
    elapsed_time = time.clock() - start
    found_solutions = expr.count_solutions()
    print 'Matrix size: ' + str(size[0]) + ' x ' + str(size[1])
    print 'Solutions found: ' + str(found_solutions)
    print 'Computation time: ' + str(round(elapsed_time, 3)) + ' s'
    with open(mhs_dir + file_name + '.mhs', mode='w') as f:
        f.write(str(expr))
    f.close()