"""Contiene metodi di utilita' per lavorare con i file"""

import os

from matrix import *

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)
    return name + '/'

def read_matrix(path):
    with open(path) as f:
        lines = f.readlines()
        rows = []
        for line in lines:
            if not line.startswith(';'):
                rows.append(line[:-2].replace(' ', ''))
    f.close()
    return Matrix(rows)