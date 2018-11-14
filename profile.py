from memory_profiler import memory_usage
from pathlib import Path
from register import REGISTRATION

def profile_repo(repo_path):
    res = {}
    for day in REGISTRATION:
        print('Profiling {}'.format(day))
        res[day] = {}

        DUT = REGISTRATION[day]

        input = get_input(1)

        res[day]['Memory'] = memory_usage((DUT,(),{'input': input}), max_usage=True)[0]

        print('Memory used: {}'.format(res[day]['Memory']))
    return res

def get_input(day):
    glob = 'day{}*.txt'.format(day)
    file = [f for f in Path(r'C:\Users\lanca_000\Documents\Software\Python\Practice\Advent of Code\2017').glob(glob)][0]
    with open(file, 'r') as f:
        return f.read()

if __name__ == '__main__':
    prof = profile_repo(Path(r'C:\Users\lanca_000\Documents\Software\Python\Practice\Advent of Code'))
    print(prof)