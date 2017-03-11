import sys
import time
import csv

from file import *
from utils import *

BITSET_BENCHMARK_DIR = 'bitset_benchmark/'
HEURISTIC_BENCHMARK_DIR = 'heuristic_benchmark/'
BENCHMARK_RESULTS_DIR = 'benchmark_results'

def show_progress(fname, partial, total):
    progress = int(round(100 * float(partial) / total))
    os.system('cls')
    print 'Progress: ' + str(progress) + '% (' + str(partial) + '/' + str(total) + ') - ' + fname

if __name__ == '__main__':
    obj = sys.argv[1]
    benchmark_results_dir = create_dir(BENCHMARK_RESULTS_DIR)
    if obj == 'b':
        matrix_files = os.listdir(BITSET_BENCHMARK_DIR)
        matrix_files.sort()
        n = len(matrix_files)
        with open(benchmark_results_dir + BITSET_BENCHMARK_DIR[:-1] + '_bool.csv', 'wb') as csvfile:
            fw = csv.writer(csvfile)
            fw.writerow(('matrix', 'time'))
            for i, matrix_file in enumerate(matrix_files):
                name = matrix_file.replace('.matrix', '')
                matrix, _ = read_matrix(BITSET_BENCHMARK_DIR + matrix_file)
                start = time.clock()
                compute_mhs(matrix)
                elapsed_time = time.clock() - start
                fw.writerow((name, str(round(elapsed_time, 3))))
                csvfile.flush()
                show_progress(name, i + 1, n)
        csvfile.close()
    elif obj == 'h':
        matrix_files = os.listdir(HEURISTIC_BENCHMARK_DIR)
        matrix_files.sort()
        n = len(matrix_files)
        with open(benchmark_results_dir + HEURISTIC_BENCHMARK_DIR[:-1] + '_h0_new.csv', 'wb') as csvfile:
            fw = csv.writer(csvfile)
            fw.writerow(('matrix', 'time'))
            for i, matrix_file in enumerate(matrix_files):
                name = matrix_file.replace('.matrix', '')
                matrix, _ = read_matrix(HEURISTIC_BENCHMARK_DIR + matrix_file)
                start = time.clock()
                compute_mhs(matrix)
                elapsed_time = time.clock() - start
                fw.writerow((name, str(round(elapsed_time, 3))))
                csvfile.flush()
                show_progress(name, i + 1, n)
        csvfile.close()
