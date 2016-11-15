from matrix import *
import sys
import re

INPUT_DIR = '../../input/'
OUTPUT_DIR = '../../output/'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]
        for fin_name in files:
            with open(fin_name + '.matrix') as f:
                lines = f.readlines()
                rows = []
                for line in lines:
                    if not line.startswith(';'):
                        rows.append(line[:-2].replace(' ', ''))
            f.close()
            matrix = Matrix(rows)
            print str(matrix)
            with open(fin_name + '.mhs', mode='w') as f:
                expr = str(compute_mhs(matrix))
                # print len(expr)
                f.write(expr)
                f.write('\n')
                f.write(str(eval(re.sub(r'[0-9]+', '1', expr))))
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