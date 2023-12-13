import re
from collections import defaultdict
from functools import reduce
from itertools import combinations
from pathlib import Path

from tqdm import tqdm


def dist(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def touched_expanders(a, b):
    # mindig b a nagyobb
    
    # touched ROWS 
    if a[0] > b[0]:
        a, b = b, a
    touched_rows = set(range(b[0], a[0], -1))
    
    if a[1] > b[1]:
        a, b = b, a
    touched_cols = set(range(b[1], a[1], -1))
    
    return touched_rows, touched_cols
    
    

def first(input):
    
    original = []
    
    for idx, line in enumerate(input.strip().split("\n")):
        #print(line)
        original.append(list(line))
        
    R, C = len(original), len(original[0])
        
    print(R, C)
    
    # expand rows
    expanded = []
    curr = 0
    while True:
        if curr == R:
            break
        row = original[curr]
        expanded.append(row)
        if set(row) == {"."}:
            expanded.append(row)
        curr += 1
        
    R = len(expanded)
    #expand cols 
    exp_cols = set()
    
    for c in range(C):
        col = [expanded[r][c] for r in range(R)]
        #print(col, set(col), c)
        if set(col) == {"."}:
            exp_cols.add(c)
            
    #print(exp_cols)
            
    
    # for row in expanded:
    #     print("".join(row))       
    
    allexp = []
    
    for r in range(R):
        
        new_row = []
        
        for c in range(C):
            new_row.append(expanded[r][c])
            if c in exp_cols:
               new_row.append(".") 
            
        allexp.append(new_row)
        
    #for row in allexp:
    #    print("".join(row))       
    
    
    gals = []
    
    for row_idx, row in enumerate(allexp):
        for col_idx, value in enumerate(row):
            if value == "#":
                gals.append((row_idx, col_idx))
                
    #print(gals)
        
    sdist = 0
    for a, b in list(combinations(gals, 2)):
        sdist += dist(a, b)
        #print(a, b, )
        
    print(sdist)
        
        
def second(input):
    
    expansion_factor = 1000000
    original = []
    exp_rows = set()
    
    for idx, line in enumerate(input.strip().split("\n")):
        print(line)
        original.append(list(line))
        if set(line) == {"."}:
            exp_rows.add(idx)
    R, C = len(original), len(original[0])
    exp_cols = set()
    
    for c in range(C):
        col = [original[r][c] for r in range(R)]
        #print(col, set(col), c)
        if set(col) == {"."}:
            exp_cols.add(c)
        
   
    print(f"rows {exp_rows}")
    print(f"cols {exp_cols}")
    
    gals = []
    for row_idx, row in enumerate(original):
        for col_idx, value in enumerate(row):
            if value == "#":
                gals.append((row_idx, col_idx))
        
    #print(gals)
    
    #sdist = 0
    sreal_dist = 0
    for a, b in tqdm(list(combinations(gals, 2))):
        TR, TC = touched_expanders(a, b)
        #distance = dist(a, b)
        #sdist += distance
        #print(a, b, distance)
        
        
        expanding_rows = TR.intersection(exp_rows)
        not_expanding_rows = TR.difference(exp_rows)
        
        expanding_cols = TC.intersection(exp_cols)
        not_expanding_cols = TC.difference(exp_cols)
        
        
        #print("NOT EXPANDING")
        #print(not_expanding_rows, not_expanding_cols)
        #print("EXPANDING")
        #print(expanding_rows, expanding_cols)
        
        real_dist = len(not_expanding_rows) + len(not_expanding_cols) + (expansion_factor * (len(expanding_rows)  + len(expanding_cols)))
        #print(f"real_dist {real_dist}")
        #print("*"*50)
        sreal_dist += real_dist
        
    print(sreal_dist)
            
if __name__ == "__main__":
    data = Path("day11.input").read_text().strip()
    
    example = """
    ...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
    
    """
    
    #first(data)
    
    # 59539038 TOO LOW
    
    second(data)