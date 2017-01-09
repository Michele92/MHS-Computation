"""Contiene l'invocazione all'algoritmo che calcola l'espressione dei minimal hitting set"""

import re
import sys
import time

from file import *
from utils import *

MATRIX_DIR = 'matrix/'
MHS_DIR = 'mhs'

if __name__ == '__main__':
    file_name = sys.argv[1]
    matrix = read_matrix(MATRIX_DIR + file_name + '.matrix')
    mhs_dir = create_dir(MHS_DIR)
    start = time.clock()
    expr = compute_mhs(matrix)
    elapsed_time = time.clock() - start
    found_solutions = eval(re.sub(r'[0-9]+', '1', str(expr)))
    print 'Found ' + str(found_solutions) + ' solutions in ' + str(round(elapsed_time, 3)) + ' seconds'
    with open(mhs_dir + file_name + '.mhs', mode='w') as f:
        f.write(str(expr))
    f.close()
