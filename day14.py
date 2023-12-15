import re
from collections import Counter
from functools import reduce
from itertools import pairwise
from pathlib import Path
from time import perf_counter

import numpy as np


def contribution(number_of_Os, number_of_rows, idx_of_max):
    return sum(range(number_of_rows - number_of_Os + 1 - idx_of_max, number_of_rows + 1 - idx_of_max))

def calculate_contrib(arr, R, idx_of_max):
    elems_counter = Counter(arr)
    print(elems_counter)

    contrib = contribution(elems_counter["O"], R, idx_of_max=idx_of_max)
    print(f"{idx_of_max=} {contrib=}")
    return contrib








def first(input):

    M = []

    for idx, line in enumerate(input.strip().split("\n")):
        print(line)
        M.append(list(line))
    R, C = len(M), len(M[0])
    print(R, C)
    _sum = 0
    start = perf_counter()
    for c in range(R):
        col = [M[r][c] for r in range(R)]

        max_idx = 0
        for idx, value in enumerate(col):
            if value == "O":
                _sum += (R - max_idx)
                max_idx += 1
            elif value == ".":
                continue
            elif value == "#":
                max_idx = idx + 1
    end = perf_counter()
    print((end-start)*1000)
    print(_sum)

def calculate_weight(M):
    R, C = len(M), len(M[0])

    _sum = 0
    for c in range(R):
        col = [M[r][c] for r in range(R)]
        max_idx = 0
        for idx, value in enumerate(col):
            if value == 0:
                _sum += (R - max_idx)
                max_idx += 1
            elif value == 1:
                continue
            elif value == 8:
                max_idx = idx + 1
    return _sum


def calculate_weight_2(M):
    _sum = 0
    for idx, row in enumerate(M):
        c = Counter(row)
        if 0 in c:
            _sum += (c[0]) * (len(M) - idx)
    return _sum


def translate_to_numpy(val):
    if val == "#":
        return 8
    elif val == ".":
        return 1
    elif val == "O":
        return 0


def move_to_last(row_segment):
    left = 0
    right = len(row_segment) - 1
    
    while left < right:
        while left < right and row_segment[right] == 0:
            right -= 1
        if row_segment[left] == 0:
            row_segment[left], row_segment[right] = row_segment[right], row_segment[left]
        left += 1
    return row_segment
        
        
        
def tilt_row(row):
    ht = [idx for idx, val in enumerate(row) if val == 8] 
    new_row = []
    if ht:
        for a, b in pairwise([0] + ht + [len(row)]):
            if b - a == 1 and not a == 0 and b==1:
                new_row += [8]
            else:
                if b != a:
                    new_row += move_to_last(row[a:b])
        return new_row
    else:
        return move_to_last(row)     


def tilt_matrix_to_the_right(matrix):
    for r in range(len(matrix)):
        matrix[r] = tilt_row(list(matrix[r]))
    

def one_cycle(matrix):
    for _ in range(4):
        matrix = np.rot90(matrix, k=1, axes=(1, 0))

def hash_of_matrix(matrix):
    return hash(tuple(matrix.ravel()))


def second(input):
    M = []

    for idx, line in enumerate(input.strip().split("\n")):
        #print(line)
        M.append(list(line))
    R, C = len(M), len(M[0])

    NM = np.zeros((R, C))
    
    
    
    for r in range(R):
        for c in range(C):
            NM[r][c] = translate_to_numpy(M[r][c])
    #NM = np.array([[1,0,1]])
    print("original")
    print(NM)
    print("*****START THE CYCLE*******--")
    
    set_of_matrix_hashes = {}
    matrix_hash_order = []
    
    for cyc in range(1000):
        for _ in range(4):
            NM = np.rot90(NM, k=1, axes=(1, 0))
            tilt_matrix_to_the_right(NM)
            #print("**************")
        #NM = np.rot90(NM, k=1, axes=(0, 1))
        #print(NM)
        
        #print(calculate_weight_2(NM))
        curr_hash = hash_of_matrix(NM)
        print(curr_hash, calculate_weight_2(NM))
        
        if curr_hash in set_of_matrix_hashes:
            print("found cycle!")
            matrix_hash_order.append("####")
            #print(set_of_matrix_hashes, curr_hash)
            
        
        W = calculate_weight_2(NM)
        set_of_matrix_hashes[curr_hash] = W 
        matrix_hash_order.append(W)
        
        print(f"CYCLE {cyc} ends...")
    print(len(matrix_hash_order), len(set_of_matrix_hashes))
    print(matrix_hash_order)
    #print(matrix_hash_order[1000000000%(len(matrix_hash_order)-1)])
    #print(Counter([value for idx, value in enumerate(matrix_hash_order) if value == 99129]))
    #bil = 1_000_000_000
    #start_idx_of_pattern = 12
    #print(matrix_hash_order[bil - (start_idx_of_pattern * (bil // (start_idx_of_pattern))) + 1])
        
        

# U, L, D, R


if __name__ == "__main__":
    data = Path("day14.input").read_text().strip()
    example = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
    """
    [34, 27, 17, 10, 8, 7, 7, 14, 0, 12]
    
    # 107059 too high
    #  99265 too high
    #  99129 too high 
    
    second(data)