import json
import sys

def write_json_sets_to_file(fname, json):
    with open(fname + '.json', mode='w') as f:
        f.write(json)
    f.close()

def count_solutions_from_json_file(fname):
    with open('json/' + fname + '.json') as f:
        solutions = json.load(f)
    f.close()
    return len(solutions['transversals'])

if __name__ == '__main__':
    print count_solutions_from_json_file(sys.argv[1])
