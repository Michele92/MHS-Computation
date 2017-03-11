import sys
import numpy as np

from file import *

div100 = lambda x: x / 100.

# bitset benchmark (b)
BITSET_TYPE = 'b'
B_BENCHMARK_DIR = 'bitset_benchmark'
B_MATRICES_PER_CONFIGURATION = 10
B_SIZES = [(10, 10), (15, 15), (20, 20), (25, 25)]
B_P1 = map(div100, range(30, 50+1, 20))

# heuristic benchmark (h)
HEURISTIC_TYPE = 'h'
H_BENCHMARK_DIR = 'heuristic_benchmark'
H_MATRICES_PER_CONFIGURATION = 30
H_SIZE = (10, 35)
H_P1 = map(div100, range(20, 80+1, 20))


#############################################
MATRICES_PER_CONFIGURATION = 10

# percentage of "1" - 1 (p1-1)
PERCENTAGE_OF_1_1_TYPE = 'p1-1'
P1_1_BENCHMARK_DIR = 'percentage_1_1_benchmark'
P_1_1_SIZE = (15, 45)
P1_1_P1 = map(div100, range(5, 95+1, 5))

# percentage of "1" - 2 (p1-2)
PERCENTAGE_OF_1_2_TYPE = 'p1-2'
P1_2_BENCHMARK_DIR = 'percentage_1_2_benchmark'
P_1_2_SIZE = (90, 30)
P1_2_P1 = map(div100, range(5, 95+1, 5))

# percentage of "1" - 3 (p1-3)
PERCENTAGE_OF_1_3_TYPE = 'p1-3'
P1_3_BENCHMARK_DIR = 'percentage_1_3_benchmark'
P_1_3_SIZE = (30, 30)
P1_3_P1 = map(div100, range(5, 95+1, 5))

# cols (c)
COLS_TYPE = 'c'
C_BENCHMARK_DIR = 'cols_benchmark'
C_ROWS = 15
C_COLS = range(15, 55+1, 10)
C_P1 = 0.25

# cols (c)
ROWS_TYPE = 'r'
R_BENCHMARK_DIR = 'rows_benchmark'
R_ROWS = range(30, 110+1, 20)
R_COLS = 30
R_P1 = 0.3

# size (s)
SIZE_TYPE = 's'
S_BENCHMARK_DIR = 'size_benchmark'
S_SIZES = [(15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (40, 40)]
S_P1 = 0.3

def generate_random_matrix(name, (nrows, ncols), p1):
    with open(name + '.matrix', mode='w') as f:
        i = 0
        while i < nrows:
            row = ' '.join([str(np.random.choice([0, 1], p=[1 - p1, p1])) for _ in range(ncols)])
            if '1' in row:
                f.write(row + '-\n')
                i += 1
    f.close()

if __name__ == '__main__':
    obj = sys.argv[1]
    if obj == BITSET_TYPE:
        b_benchmark_dir = create_dir(B_BENCHMARK_DIR)
        n = B_MATRICES_PER_CONFIGURATION * len(B_SIZES) * len(B_P1)
        _id = 1
        for size in B_SIZES:
            for p1 in B_P1:
                for i in range(B_MATRICES_PER_CONFIGURATION):
                    name = b_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * p1))
                    generate_random_matrix(name, size, p1)
                    _id += 1
    elif obj == HEURISTIC_TYPE:
        h_benchmark_dir = create_dir(H_BENCHMARK_DIR)
        n = H_MATRICES_PER_CONFIGURATION * len(H_P1)
        _id = 1
        size = H_SIZE
        for p1 in H_P1:
            for i in range(H_MATRICES_PER_CONFIGURATION):
                name = h_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * p1))
                generate_random_matrix(name, size, p1)
                _id += 1
    elif obj == PERCENTAGE_OF_1_1_TYPE:
        p1_1_benchmark_dir = create_dir(P1_1_BENCHMARK_DIR)
        n = MATRICES_PER_CONFIGURATION * len(P1_1_P1)
        _id = 1
        size = P_1_1_SIZE
        for p1 in P1_1_P1:
            for i in range(MATRICES_PER_CONFIGURATION):
                name = p1_1_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * p1))
                generate_random_matrix(name, size, p1)
                _id += 1
    elif obj == PERCENTAGE_OF_1_2_TYPE:
        p1_2_benchmark_dir = create_dir(P1_2_BENCHMARK_DIR)
        n = MATRICES_PER_CONFIGURATION * len(P1_2_P1)
        _id = 1
        size = P_1_2_SIZE
        for p1 in P1_2_P1:
            for i in range(MATRICES_PER_CONFIGURATION):
                name = p1_2_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * p1))
                generate_random_matrix(name, size, p1)
                _id += 1
    elif obj == PERCENTAGE_OF_1_3_TYPE:
        p1_3_benchmark_dir = create_dir(P1_3_BENCHMARK_DIR)
        n = MATRICES_PER_CONFIGURATION * len(P1_3_P1)
        _id = 1
        size = P_1_3_SIZE
        for p1 in P1_3_P1:
            for i in range(MATRICES_PER_CONFIGURATION):
                name = p1_3_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * p1))
                generate_random_matrix(name, size, p1)
                _id += 1
    elif obj == COLS_TYPE:
        c_benchmark_dir = create_dir(C_BENCHMARK_DIR)
        n = MATRICES_PER_CONFIGURATION * len(C_COLS)
        _id = 1
        for cols in C_COLS:
            size = (C_ROWS, cols)
            for i in range(MATRICES_PER_CONFIGURATION):
                name = c_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * C_P1))
                generate_random_matrix(name, size, C_P1)
                _id += 1
    elif obj == ROWS_TYPE:
        r_benchmark_dir = create_dir(R_BENCHMARK_DIR)
        n = MATRICES_PER_CONFIGURATION * len(R_ROWS)
        _id = 1
        for rows in R_ROWS:
            size = (rows, R_COLS)
            for i in range(MATRICES_PER_CONFIGURATION):
                name = r_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * C_P1))
                generate_random_matrix(name, size, R_P1)
                _id += 1
    elif obj == SIZE_TYPE:
        s_benchmark_dir = create_dir(S_BENCHMARK_DIR)
        n = MATRICES_PER_CONFIGURATION * len(S_SIZES)
        _id = 1
        for size in S_SIZES:
            for i in range(MATRICES_PER_CONFIGURATION):
                name = s_benchmark_dir + str(_id).zfill(3) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + str(int(100 * S_P1))
                generate_random_matrix(name, size, S_P1)
                _id += 1
