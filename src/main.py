from matrix import *

# matrice di 'tema.pdf'
m1 = ['1000101',
      '1010001',
      '0101001',
      '1101000',
      '1010001',
      '0101100',
      '1000001']

# matrice di 'elaborato2015_16.pdf'
m2 = ['00110',
      '11010',
      '01111']

# matrice del paper su STACCATO
m3 = ['10011',
      '01101',
      '00101',
      '10001',
      '00111',
      '00111',
      '00111']

m4 = ['000100',
      '111001',
      '001111',
      '000010',
      '111010']

m = Matrix(m4)
print 'Matrice originale'
print str(m)
print str(compute_mhs(m))

# n = len([f for input_dir in os.listdir('input') for f in os.listdir('input/' + input_dir)])
# for i, input_dir in enumerate(os.listdir('input')):
#     output_dir = create_dir('output/results' + input_dir[-1])
#     m = len(os.listdir('input/' + input_dir))
#     for j, benchmark in enumerate(os.listdir('input/' + input_dir)):
#         fin_name = 'input/' + input_dir + '/' + benchmark
#         with open(fin_name) as f:
#             lines = f.readlines()
#             rows = []
#             for line in lines:
#                 if not line.startswith(';'):
#                     rows.append(line[:-2].replace(' ', ''))
#         f.close()
#         matrix = Matrix(rows)
#         mhs = matrix.compute_mhs()
#         show_progress(fin_name, i * m + (j + 1), n)
#         with open(output_dir + benchmark.replace('matrix', 'mhs'), mode='w') as f:
#             f.write(clean_expression(mhs))
#         f.close()