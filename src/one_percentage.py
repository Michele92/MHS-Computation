from file import *
import csv

BENCHMARK_DIR = '../../benchmarks/'
ONE_PERCENTAGE_DIR = 'one_percentage'

def get_one_percentage(path):
    with open(path) as f:
        lines = f.readlines()
        rows = []
        ones = 0
        for line in lines:
            if not line.startswith(';'):
                bitstring = line[:-2].replace(' ', '')
                rows.append(bitstring)
                ones += bitstring.count('1')
    f.close()
    size = len(rows) * len(rows[0])
    return round(100 * float(ones) / size, 3)

if __name__ == '__main__':
    one_percentage_dir = create_dir(ONE_PERCENTAGE_DIR)
    groups_dirs = os.listdir(BENCHMARK_DIR)
    for group_dir in groups_dirs:
        with open(one_percentage_dir + group_dir + '.csv', 'wb') as csvfile:
            fw = csv.writer(csvfile)
            fw.writerow(('matrix', 'one_percentage'))
            matrix_files = os.listdir(BENCHMARK_DIR + group_dir)
            matrix_files.sort()
            for matrix_file in matrix_files:
                name = matrix_file.replace('.matrix', '')
                fw.writerow((name, str(get_one_percentage(BENCHMARK_DIR + group_dir + '/' + matrix_file)) + '%'))
        csvfile.close()
