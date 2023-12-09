import re
from collections import defaultdict
from functools import reduce
from itertools import pairwise
from pathlib import Path


def make_sequence(line):
    return [int(x) for x in line.split(" ") if x != ""]

def expand_deltas(seq):
    delta_seq = [b - a for a, b in pairwise(seq)]
    return delta_seq

def expand_until_zeros(seq):
    expands = [seq]
    while not all(s==0 for s in seq):
        seq = expand_deltas(seq)
        expands.append(seq)
    return expands


def first(input):
    sums = 0
    for idx, line in enumerate(input.strip().split("\n")):
        seq = make_sequence(line)
        expands = expand_until_zeros(seq)
        print(expands)
        sums += sum(x[-1] for x in expands)
    print(sums)
        
def second(input):
    last_numbers = []
    for idx, line in enumerate(input.strip().split("\n")):
        seq = make_sequence(line)
        expands = expand_until_zeros(seq)
        #print(expands)
        last_numbers.append([x[0] for x in expands[::-1]])
    print(last_numbers)
    
    sums = 0
    for last in last_numbers:
        extr = reduce(lambda x, y: y - x, last)
        sums += extr
    print(sums)
    
            
if __name__ == "__main__":
    data = Path("day9.input").read_text().strip()
    
    example = """
    0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
    """
    
    example_2 = """
        0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
    """
    
    #first(example)
    #first(data)
     #second(example_2)
    second(data)