import re
import time

from json_sets import *
from matrix import *

INPUT_DIR = '../../input/'
OUTPUT_DIR = '../../output/'
MATRIX_DIR = 'matrix/'
MHS_DIR = 'mhs'
JSON_DIR = 'json'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]
        for fin_name in files:
            with open(MATRIX_DIR + fin_name + '.matrix') as f:
                lines = f.readlines()
                rows = []
                for line in lines:
                    # if not line.startswith('0') and not line.startswith('1'):
                    #     break
                    if not line.startswith(';'):
                        rows.append(line[:-2].replace(' ', ''))
            f.close()
            # print len(rows)
            matrix = Matrix(rows)
            # print len(matrix.rows)
            # exit()
            json_dir = create_dir(JSON_DIR)
            write_json_sets_to_file(json_dir + fin_name, matrix.to_json())
            mhs_dir = create_dir(MHS_DIR)
            with open(mhs_dir + fin_name + '.mhs', mode='w') as f:
                start = time.clock()
                expr = compute_mhs(matrix)
                print str(time.clock() - start)
                f.write(str(expr))
                # f.write(re.sub("(.{100})", "\\1\n", str(expr), 0, re.DOTALL))
                f.write('\n')
                f.write(str(eval(re.sub(r'[0-9]+', '1', str(expr)))))
            f.close()
    else:
        n = len([f for input_dir in os.listdir(INPUT_DIR) for f in os.listdir(INPUT_DIR + input_dir)])
        for i, input_dir in enumerate(os.listdir(INPUT_DIR)):
            output_dir = create_dir(OUTPUT_DIR + 'results' + input_dir[-1])
            m = len(os.listdir(INPUT_DIR + input_dir))
            for j, benchmark in enumerate(os.listdir(INPUT_DIR + input_dir)):
                fin_name = INPUT_DIR + input_dir + '/' + benchmark
                with open(fin_name) as f:
                    lines = f.readlines()
                    rows = []
                    for line in lines:
                        if not line.startswith(';'):
                            rows.append(line[:-2].replace(' ', ''))
                f.close()
                matrix = Matrix(rows)
                show_progress(fin_name, i * m + (j + 1), n)
                with open(output_dir + benchmark.replace('matrix', 'mhs'), mode='w') as f:
                    f.write(str(compute_mhs(matrix)))
                f.close()