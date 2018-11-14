from memory_profiler import profile
from pathlib import Path
import os

def profile_by_day(day):
    def aoc_profile(solution_func):
        def prof(input=None):
            print('Start profile')
            print('Day {}'.format(day))

            if input is None:
                with open(Path(os.getcwd()) / 'day{}.txt'.format(day), 'r') as file:
                    return solution_func(file.read())
            else:
                return solution_func(input)

            print('End profile')
        return prof
    return aoc_profile

@profile_by_day(day=2)
def test_sol(input):
    print('The start of the puzzle input is:\n{}'.format(input))

if __name__ == '__main__':
    test_sol()