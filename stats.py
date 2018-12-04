from pathlib import Path
import cProfile
import pstats
import sys
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import prof

def collect_stats(solution, input_path, n=1000):
    inputs = solution[0].split('.')
    year = int(inputs[0])
    day = int(inputs[1])
    input_file = [f for f in input_path.glob('{}/*day*{}*.txt'.format(year, day))][0]
    with open(input_file, 'r') as file:
        input = file.read()

    res = np.empty(n)
    start = datetime.now()
    for i in range(n):
        cProfile.runctx('solution[1](input)', globals=globals(), locals=locals(), filename='cstats')
        stats = pstats.Stats('cstats')
        t = prof.extract_time(stats, solution[1])
        res[i] = t
    return start, res

if __name__ == '__main__':
    from register import REGISTRATION
    start, times = collect_stats(REGISTRATION[-1], Path(r'C:\Users\lancasj\Documents\Python\AoC-Benchmark\AoC-Inputs'), 10)
    for t in times[:5]: print(t)