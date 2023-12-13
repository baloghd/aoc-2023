import re
from collections import defaultdict
from functools import reduce
from pathlib import Path


def find_horizontal_reflection(pattern):
    line_hashes = defaultdict(set)
    h_candidates = []
    for idx, line in enumerate(pattern):
        h = hash(tuple(line))
        if (h in line_hashes) and (idx - 1 in line_hashes[h]):
            h_candidates.append([idx - 1, idx])
        line_hashes[h].add(idx)
    return h_candidates

def find_vertical_reflection(pattern):
    col_hashes = defaultdict(set)
    R, C = len(pattern), len(pattern[0])
    v_candidates = []
    for c in range(C):
        col = [pattern[r][c] for r in range(R)]
        h = hash(tuple(col))
        if (h in col_hashes) and (c - 1 in col_hashes[h]):
            v_candidates.append([c - 1, c])
        col_hashes[h].add(c)
    return v_candidates
                        

def check_horizontal_candidate(pattern, candidate):
    #line_hash_map = {}
    U, D = candidate
    
    if D == len(pattern) - 1 and U == len(pattern) - 2:
        #print("szélsőHORIZTONAL")
        return True
    
    true_mirror = True
    while U >= 0 and D < len(pattern):
        hU = hash(tuple(pattern[U]))
        hD = hash(tuple(pattern[D]))
        if hU == hD:
            U -= 1
            D += 1
        else:
            true_mirror = False
            break
    return true_mirror

def check_vertical_candidate(pattern, candidate):
    num_rows = len(pattern)
    L, R = candidate
    
    if R == len(pattern[0]) - 1 and L == len(pattern[0]) - 2:
        #print("szélsőVERTICAL")
        return True
    
    
    true_mirror = True
    while L >= 0 and R < len(pattern[0]):
        hL = hash(tuple([pattern[row][L] for row in range(num_rows)]))
        hR = hash(tuple([pattern[row][R] for row in range(num_rows)]))
        if hL == hR:
            L -= 1
            R += 1
        else:
            true_mirror = False
            break
    return true_mirror


def flip_smudge(val):
    return "." if val == "#" else "#"

def generate_smudge_alternatives(pattern):
    R, C = len(pattern), len(pattern[0])
    for r in range(R):
        for c in range(C):
            pattern[r][c] = flip_smudge(pattern[r][c])
            yield pattern
            pattern[r][c] = flip_smudge(pattern[r][c])
        

def first(input):
    pat = defaultdict(list)
    pat_idx = 0
    for idx, line in enumerate(input.strip().split("\n")):
        if line == "":
            pat_idx += 1
            continue
        pat[pat_idx].append(line)
        
    #print(pat)
    _sum = 0
    for pat_idx, curr_pat in pat.items():
        print(pat_idx, curr_pat)
        h_candidates = find_horizontal_reflection(curr_pat)
        v_candidates = find_vertical_reflection(curr_pat)
        
        #print("horizontal")
        #print("vertical")
        
        
        if h_candidates:
            for h_candidate in h_candidates:
                is_h = check_horizontal_candidate(curr_pat, h_candidate)
                if is_h:
                    print("HORIZONTAL")
                    print(h_candidate)
                    add = (h_candidate[0] + 1) * 100
                    print(add)
                    _sum += add
        if v_candidates:
            for v_candidate in v_candidates:
                is_v = check_vertical_candidate(curr_pat, v_candidate)
                if is_v:
                    print("VERTICAL")
                    print(v_candidate)
                    add = (v_candidate[0] + 1)
                    print(add)
                    _sum += add
            
        print("****"*5)
    print(_sum)
        
        
        # print(check_vertical_candidate(curr_pat, v_candidate))
        # print("***"*10)
        
def process_pattern(curr_pat, current_mirror):    
    h_candidates = find_horizontal_reflection(curr_pat)
    v_candidates = find_vertical_reflection(curr_pat)
    if h_candidates:
        for h_candidate in h_candidates:
            is_h = check_horizontal_candidate(curr_pat, h_candidate)
            if is_h:
                #print("HORIZONTAL")
                #print(h_candidate)
                add = (h_candidate[0] + 1) * 100
                add_obj = ("H", tuple(h_candidate), add)
                if add_obj not in current_mirror:
                    current_mirror.add(add_obj)    
                #print(add)

    if v_candidates:
        for v_candidate in v_candidates:
            is_v = check_vertical_candidate(curr_pat, v_candidate)
            if is_v:
                #print("VERTICAL")
                #print(v_candidate)
                add = (v_candidate[0] + 1)
                add_obj = ("V", tuple(v_candidate), add)
                if add_obj not in current_mirror:
                    current_mirror.add(add_obj)    
                #print(add)
    return current_mirror

def second(input):
    pat = defaultdict(list)
    pat_idx = 0
    for idx, line in enumerate(input.strip().split("\n")):
        if line == "":
            pat_idx += 1
            continue
        pat[pat_idx].append(list(line))

    _sum = 0
    for pat_idx, curr_pat in pat.items():
        current_mirror = process_pattern(curr_pat, set())
        #print(current_mirror)
        
        generated_mirrors = set()
        for p in generate_smudge_alternatives(curr_pat):
            generated_mirrors = process_pattern(p, current_mirror=generated_mirrors)
        
        new_mirror = generated_mirrors - current_mirror
        #print(current_mirror, "->", new_mirror)
        _sum += list(new_mirror)[0][-1]
    
            
        #     print("****"*5)
    print(_sum)
    
 


if __name__ == "__main__":
    data = Path("day13.input").read_text().strip()
   
    example8 = """
.#####.#.#.....
##..###.#...##.
##...####....##
####.#..#.##.##
####.#..#.##.##
##...####....##
##..###.#...##.
.#####.#.##....
####..#..##.##.
#..#..#########
##.#####.#.#...
.#.##.#.#..####
##..#####....#.
..#.#.##..#....
..#.#.##..#....
"""

    example = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
    
    """
    
    example2 = """
.#####.#.#.....
##..###.#...##.
##...####....##
####.#..#.##.##
####.#..#.##.##
##...####....##
##..###.#...##.
.#####.#.##....
####..#..##.##.
#..#..#########
##.#####.#.#...
.#.##.#.#..####
##..#####....#.
..#.#.##..#....
..#.#.##..#....
    """
    
    example3 = """
    
####....###
##..####..#
.....##....
...#....#..
#..######..
.....##....
###.####.##
.###....###
.##.####.##
...#....#..
.##########
#..######..
....#..#...
    """
    
    example4 = """
#.####.#.##
#......#...
..####..#..
...##...##.
.######..##
.#.##.#.#..
###..###.##
.##..##..##
.#.##.#.#..
    """
    
    example5 = """
    
.....####......#.
#..#.####.#..#..#
......##......#.#
.....#..#.......#
#..#..##..#..#.##
#####....#####..#
.....####.......#
######..#######..
######..######.##
#####....#######.
...########....##
#..#.####.#..#.##
####.####.#######
.##.#.##.#.##...#
#..#......#..#...

    """
    
    example6 = """
    
######..#
.##...##.
#..#.####
...#.#..#
#....#.##
#....#.##
...#....#
#..#.####
.##...##.
######..#
######..#
    """
    
    example7 = """
##..##.#.#.#.
#####.#...#..
..#.##..#...#
.#....#....#.
...####.##.#.
####...##..#.
.##.#.##..#.#
.##.#.##..#.#
####...##..#.
...####.##.#.
.#..#.#....#.
..#.##..#...#
#####.#...#..
##..##.#.#.#.
#..##.....##.
###..#.#.####
###..#.#.####
    """
    
    # 12628 too low
    # 14834 too low
    # 15481 too low
    # 30121 not the right answer
    #first(example8)
    second(data)