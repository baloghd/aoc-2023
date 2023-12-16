import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from functools import reduce
from pathlib import Path

sys.setrecursionlimit(100000)

go_direction_to_orientation = {
    "R": "L",
    "L": "R",
    "U": "D",
    "D": "U"
}


# R, L, U, D
def move_dir(coords, go_direction):
    new_r, new_c = 0, 0
    r, c = coords
    match go_direction:
        case "R":
            new_r, new_c = r, c + 1
        case "L":
            new_r, new_c = r, c - 1
        case "U":
            new_r, new_c = r - 1, c
        case "D":
            new_r, new_c = r + 1, c
    return new_r, new_c

def is_valid_move(R, C, *args):
   new = move_dir(*args) 
   return (0 <= new[0] < R) and (0 <= new[1] < C)

def outcome(new_coords, direction, value):
    mirror_map = {
        "\\": {
            "R": "U",
            "L": "D",
            "U": "R",
            "D": "L"
        },
        "/": {
            "D": "R",
            "R": "D",
            "L": "U",
            "U": "L"        
        }
    }
    ori = go_direction_to_orientation[direction]
    match value:
        case ".":
            return [(new_coords, direction)]
        case "-":
            if (ori == "U") or (ori == "D"):
                return [(new_coords, "R"), (new_coords, "L")]
            elif (ori == "R") or (ori == "L"):
                return [(new_coords, direction)]
        case "|":
            if (ori == "L") or (ori == "R"):
                return [(new_coords, "U"), (new_coords, "D")]
            elif (ori == "U") or (ori == "D"):
                return [(new_coords, direction)]
        case "\\":
            return [(new_coords, mirror_map["\\"][ori])]
        case "/":
            return [(new_coords, mirror_map["/"][ori])]


# def step(current_coords, direction, R, C, visited):
#     #print(f"step({current_coords, direction, R, C, visited})")
    
#     if not is_valid_move(R, C, *(current_coords, direction)):
#         print(current_coords, direction, " HAS NO VALID MOVES")
#         print("****")
#         visited.add((current_coords, direction))
#         return 
#     next_candidate = move_dir(current_coords, direction)
#     print(f"{next_candidate=}")
#     curr_val = M[current_coords[0]][current_coords[1]]
#     val = M[next_candidate[0]][next_candidate[1]]
#     outcome_of_moves = outcome(next_candidate, direction, val)
#     if outcome_of_moves:
#         print(current_coords, direction, curr_val, "->", outcome_of_moves)
#         for oc in outcome_of_moves:
#             if oc in visited:
#                 return
#             step(*oc, R, C, visited)
#             visited.add(oc)
            

#vis = set()
#ret = step(start, direction, R, C, vis)


def iteration(M, start, direction):
    R, C = len(M), len(M[0])
    
    def run(start, direction):
        current_coords = start
        visited_in_run = set()
        new_run_starts = None
        while is_valid_move(R, C, *(current_coords, direction)):
            next_candidate = move_dir(current_coords, direction)
            curr_val = M[current_coords[0]][current_coords[1]]
            val = M[next_candidate[0]][next_candidate[1]]

            outcome_of_moves = outcome(next_candidate, direction, val)
            #print(current_coords, direction, curr_val, "->", outcome_of_moves)
            if outcome_of_moves:
                if len(outcome_of_moves) == 2:
                    #print("SPLITTER")
                    oc = outcome_of_moves[0]
                    visited_in_run.add((current_coords, direction))
                    new_run_starts = outcome_of_moves
                    return {"visited_in_run": visited_in_run, "outcome_of_moves": new_run_starts} 
                elif len(outcome_of_moves) == 1:
                    oc = outcome_of_moves[0]
                    visited_in_run.add((current_coords, direction))
                    new_run_starts = outcome_of_moves
                    current_coords = oc[0]
                    direction = oc[1]
            
        visited_in_run.add((current_coords, direction))
        return {"visited_in_run": visited_in_run, "outcome_of_moves": new_run_starts}
                
    #start, direction = (0, 0), "D"
    all_runs = defaultdict(dict)
    first = True
    outcome_of_moves = set()
    while True:
       
        if first:
            cstart, cdirection = start, direction
        #print(f"{cstart, cdirection}")
        first = False
        run_ret = run(cstart, cdirection)
        
        all_runs[(cstart, cdirection)]["visited_in_run"] = run_ret["visited_in_run"]

        if run_ret["outcome_of_moves"]:
            outcome_of_moves = outcome_of_moves.union(set(run_ret["outcome_of_moves"]))
        
        
        for (cst, cdir) in outcome_of_moves:
            if (cst, cdir) not in all_runs:
                cstart, cdirection = cst, cdir
                continue
                
        all_in = True
        for (_start, _dir) in outcome_of_moves:
            if (_start, _dir) not in all_runs:
                    all_in = False
                    
        if all_in:
            break
    #print(all_runs)
    #print(all_runs)
    vis = set()
    for k in all_runs:
        vis = vis.union(all_runs[k]["visited_in_run"])

    # M2 = deepcopy(M)
    
    # for ((r, c), _) in vis:
    #       M2[r][c] = "#"
         
    # for row in M2:
    #      print("".join(row))

    
         
    #print((start, direction) in vis)
    visited_squares = {s for (s, d) in vis}
    ooc_set = {s for (s, d) in outcome_of_moves}
    #print(ooc_set.union(visited_squares))
    return len(ooc_set.union(visited_squares))
    

def first(input):
    M = []
    for idx, line in enumerate(input.strip().split("\n")):
        #print(line)
        M.append(list(line))
        
    i = iteration(M, (109, 20), "U")
    print(i)
    
from tqdm import tqdm


def second(input):
    M = []
    for idx, line in enumerate(input.strip().split("\n")):
        #print(line)
        M.append(list(line))
        
    R, C = len(M), len(M[0])
    _max = 0
    max_config = None
    _is = []
    for r in range(R):
        for c in range(C):
            if r == 0:
                print((r, c), "D")
                i = iteration(M, (r, c), "D")
                if i > _max:
                    _max = i
                    max_config = (r, c), "D"
                print(i, _max)
                _is.append(i)
    for r in range(R):
        for c in range(C):
            if r == R - 1:
                print((r, c), "U")
                i = iteration(M, (r, c), "U")
                if i > _max:
                    _max = i
                    max_config = (r, c), "U"
                print(i, _max)
                _is.append(i)
            #elif r == R - 1:
            #     print((r, c))
            # #     #i = iteration(M, (r, c), "U")
            # #     #_max = max(_max, i)
    for r in range(R):
        for c in range(C):
            if c == 0:
                print((r, c), "R")
                i = iteration(M, (r, c), "R")
                if i > _max:
                    _max = i
                    max_config = (r, c), "R"
                print(i, _max)
                _is.append(i)
    for r in range(R):
        for c in range(C):
            if c == C - 1:
                print((r, c), "L")
                i = iteration(M, (r, c), "L")
                if i > _max:
                    _max = i
                    max_config = (r, c), "L"
                print(i, _max)
                _is.append(i)
            #     print((r, c))
            # #     #i = iteration(M, (r, c), "R")
            # #     #_max = max(_max, i)
            # elif c == C - 1:
            #     print((r, c))
                #i = iteration(M, (r, c), "L")
                #_max = max(_max, i)
    
    print(_max)
    print(max_config)
    print(sorted(_is))
            
if __name__ == "__main__":
    data = Path("day16.input").read_text().strip()
    
    example = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
    """
    #first(data)
    
    # 7668 too low
    # 7694 too low
    # 7743 too high
    # 7742 not the right answer
    # 7715 not the right answer
    
    second(data)