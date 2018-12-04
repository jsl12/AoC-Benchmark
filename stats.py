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
    input = prof.get_input(solution[0], input_path)
    res = np.empty(n)
    start = datetime.now()
    for i in range(n):
        cProfile.runctx('solution[1](input)', globals=globals(), locals=locals(), filename='cstats')
        stats = pstats.Stats('cstats')
        t = prof.extract_time(stats, solution[1])
        res[i] = t
    return start, res

def collect_dataframe(*args):
    start, res = collect_stats(*args)
    df = pd.DataFrame(res, columns=['Execution Duration [ms]'])
    df.index.name = 'Run #'
    return start, df

if __name__ == '__main__':
    from register import REGISTRATION
    start, df = collect_dataframe(REGISTRATION[-1], Path(r'C:\Users\lanca_000\Documents\Software\Python\AoC Benchmark\AoC-Inputs'), 10)
    print(df.mean()[0])
    df.to_csv('stats.csv')
    # for t in times: print(t)