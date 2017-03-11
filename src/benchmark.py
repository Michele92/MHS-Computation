import csv
import time

from file import *
from utils import *

# MATRIX_DIR = '74L85'
# MATRIX_DIR = '74181'
# MATRIX_DIR = '74182'
# MATRIX_DIR = '74283'
# MATRIX_DIR = 'c432'
# MATRIX_DIR = 'c499'
# MATRIX_DIR = 'c880'
# MATRIX_DIR = 'c1355'
# MATRIX_DIR = 'c1908'
# MATRIX_DIR = 'c2670'
# MATRIX_DIR = 'c3540'
MATRIX_DIR = 'c5315'
# MATRIX_DIR = 'c6288'
# MATRIX_DIR = 'c7552'

ROWS_TO_EXCLUDE = []
MATRICES_TO_EXCLUDE = []

BENCHMARK_DIR = '../../benchmarks/' + MATRIX_DIR + '/'
BENCHMARK_RESULTS_DIR = 'benchmark_results'

def show_progress(fname, partial, total):
    progress = int(round(100 * float(partial) / total))
    os.system('cls')
    print 'Progress: ' + str(progress) + '% (' + str(partial) + '/' + str(total) + ') - ' + fname

if __name__ == '__main__':
    benchmark_results_dir = create_dir(BENCHMARK_RESULTS_DIR)
    matrix_files = os.listdir(BENCHMARK_DIR)
    matrix_files.sort()
    n = len(matrix_files)
    with open(benchmark_results_dir + MATRIX_DIR + 'cp.csv', 'wb') as csvfile:
        fw = csv.writer(csvfile)
        fw.writerow(('matrix', 'rows', 'cols', 'solutions', 'time'))
        for i, matrix_file in enumerate(matrix_files):
            matrix, size = read_matrix(BENCHMARK_DIR + matrix_file)
            name = matrix_file.replace('.matrix', '')
            # if size[0] > 30 or size[0] in ROWS_TO_EXCLUDE:
            # if size[0] >= 32 or int(name[-3:]) in MATRICES_TO_EXCLUDE:
            #     elapsed_time = 'timeout'
            #     found_solutions = 'NaN'
            # else:
            try:
                start = time.clock()
                expr = compute_mhs(matrix)
                elapsed_time = round(time.clock() - start, 3)
                found_solutions = expr.count_solutions()
            except multiprocessing.TimeoutError:
                elapsed_time = 'timeout'
                found_solutions = 'NaN'
            fw.writerow((name, str(size[0]), str(size[1]), str(found_solutions), str(elapsed_time)))
            csvfile.flush()
            show_progress(name, i + 1, n)
    csvfile.close()
