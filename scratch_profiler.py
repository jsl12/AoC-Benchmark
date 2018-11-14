# from pathlib import Path
# import os
from memory_profiler import memory_usage, profile
from register import REGISTRATION

def main():
    with open(r'C:\Users\lanca_000\Documents\Software\Python\Practice\Advent of Code\2017\day1.txt', 'r') as file:
        input = file.read()

    f = REGISTRATION['day1.1']

    mem_usage = memory_usage((f, (), {'input':input}), max_usage=True)

    return mem_usage

if __name__ == "__main__":
    print(main())