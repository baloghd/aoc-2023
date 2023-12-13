import re
from collections import Counter, defaultdict
from copy import deepcopy
from functools import reduce
from itertools import pairwise
from pathlib import Path

import networkx as nx
from tqdm import tqdm

D = {
    "up": [-1, 0], # fel
    "down": [1, 0], # le
    "left": [0, -1], # bal
    "right": [0, 1], # jobbra
}

valid_directions = {
    "F": ["right", "down"],
    "7": ["left", "down"],
    "J": ["up", "left"],
    "L": ["up", "right"],
    "|": ["up", "down"],
    "-": ["left", "right"],
    ".": []
}

opposites = {
    "right": "left",
    "left": "right",
    "up": "down",
    "down": "up"
}

def matrix_to_node(i, j, num_cols):
    return i * num_cols + j

def node_to_matrix(node, num_rows, num_cols):
    r = node // num_rows
    return [r, node - (r*num_rows)]


from termcolor import colored


def print_colored_string(input_string):
    colored_string = ""

    for char in input_string:
        if char == '.':
            colored_string += colored(char, 'red')
        elif char == "#":
            colored_string += colored(char, "cyan")
        elif char in {"┌", "┐", "└", "┘", "-", "|"}:
            colored_string += colored(char, "green")
        else:
            colored_string += char

    print(colored_string)

def first_second(input):
    # sor, oszlop!
    M = []
    Scoord = []
    points = 0
    for idx, line in enumerate(input.strip().split("\n")):
        if "S" in line:
            print("#"*140)
            Scoord = [idx, line.index("S")]
        
        points += Counter(line)["."]
        M.append(list(line))
        print(line, idx)
        
    R, C = len(M), len(M[0])
    print(R, C, R*C, points, points/(R*C))
    #print(M)
    
    edges = []
    
    for row_idx, row in enumerate(M):
        for col_idx, value in enumerate(row):
            
            if value == ".":
                continue
            
            starting_dirs = []
            if value == "S":
                continue
                
            for _dir in valid_directions[value]:
                d = D[_dir]
                
                if (row_idx == 0) and  (_dir == "up"): # check row above
                    continue
                
                if (row_idx == R - 1) and (_dir == "down"): # check row below
                    continue
                
                if (col_idx == 0) and (_dir == "left"):
                    continue
                
                if (col_idx == C - 1) and (_dir == "right"):
                    continue 
                #print(row_idx, col_idx, d)
                _to_value = M[row_idx + d[0]][col_idx + d[1]]
                
                if _to_value == "S":
                    continue
                
                if opposites[_dir] in valid_directions[_to_value]:
                    # can go that way!
                    edges.append([matrix_to_node(row_idx, col_idx, R), matrix_to_node(row_idx + d[0], col_idx + d[1], R)])
    
    
     
     # add start
    Sr, Sc = Scoord
    
    Sdirs = []
    if M[Sr-1][Sc] in {"F", "7", "|"}:
        Sdirs.append("up")
    if M[Sr+1][Sc] in {"J", "L", "|"}:
        Sdirs.append("down")
    if M[Sr][Sc-1] in {"F", "L", "-"}:
        Sdirs.append("left")
    if M[Sr][Sc+1] in {"J", "7", "-"}:
        Sdirs.append("right")

    print(Scoord, Sdirs) 
    print(matrix_to_node(*Scoord, C))
    #print(node_to_matrix(matrix_to_node(*Scoord, R), R, C))

    
    # S = 9748
    
    # edges.append([9748, 9749])
    # edges.append([9888, 9748])
    
    #print(edges)
    G = nx.Graph(edges)
    print(G.nodes)
    cycle = list(nx.chordless_cycles(G))
    print(len(cycle))
    
    if 9748 in G.nodes:
        print("innit")
    
    
    the_cycle = None
    
    for c in cycle:
        if 9748 in c:
            print(len(c)  //2  )
            the_cycle = c
            
    
    node_coords = []
    if the_cycle:
        for node in the_cycle:
            node_coords.append(node_to_matrix(node, R, C))
    

    print(node_coords)
    


def second(input):
        # sor, oszlop!
    M = []
    Scoord = []
    points = 0
    for idx, line in enumerate(input.strip().split("\n")):
        if "S" in line:
            print("#"*140)
            Scoord = [idx, line.index("S")]
        
        points += Counter(line)["."]
        M.append(list(line))
        print(line, idx, matrix_to_node(idx, 0, 20))
        
    R, C = len(M), len(M[0])
    print(R, C, R*C, points, points/(R*C))
    #print(M)
    
    edges = []
    
    for row_idx, row in enumerate(M):
        for col_idx, value in enumerate(row):
            
            if value == ".":
                continue
            
            starting_dirs = []
            if value == "S":
                continue
                
            for _dir in valid_directions[value]:
                d = D[_dir]
                
                if (row_idx == 0) and  (_dir == "up"): # check row above
                    continue
                
                if (row_idx == R - 1) and (_dir == "down"): # check row below
                    continue
                
                if (col_idx == 0) and (_dir == "left"):
                    continue
                
                if (col_idx == C - 1) and (_dir == "right"):
                    continue 
                #print(row_idx, col_idx, d)
                _to_value = M[row_idx + d[0]][col_idx + d[1]]
                
                if _to_value == "S":
                    continue
                
                if opposites[_dir] in valid_directions[_to_value]:
                    # can go that way!
                    edges.append([matrix_to_node(row_idx, col_idx, R), matrix_to_node(row_idx + d[0], col_idx + d[1], R)])
    
     
     # add start
    Sr, Sc = Scoord
    
    Sdirs = []
    if M[Sr-1][Sc] in {"F", "7", "|"}:
        Sdirs.append("up")
    if M[Sr+1][Sc] in {"J", "L", "|"}:
        Sdirs.append("down")
    if M[Sr][Sc-1] in {"F", "L", "-"}:
        Sdirs.append("left")
    if M[Sr][Sc+1] in {"J", "7", "-"}:
        Sdirs.append("right")

    print(Scoord, Sdirs) 
    print(matrix_to_node(*Scoord, C))
    #print(node_to_matrix(matrix_to_node(*Scoord, R), R, C))

    
    #edges.append([12, 13])
    #edges.append([12, 22])
    
    
    #edges.append([92, 93])
    #edges.append([92, 102])
    
    
    # S = 9748
    
    edges.append([9748, 9749])
    edges.append([9888, 9748])
    
    #print(edges)
    G = nx.Graph(edges)
    #print(G.nodes)
    cycle = list(nx.chordless_cycles(G))
    print(len(cycle))
    
    if 9748 in G.nodes:
        print("innit")
    
    
    the_cycle = None
    
    for c in cycle:
        if 9748 in c:
            print("innit the cacyle")
            the_cycle =c
    print(len(the_cycle))
    print(the_cycle[:20])
    #print(list(nx.all_simple_paths(G, 9748, 9748)))
    
    #print(the_cycle)
    # the_cycle_coords = {tuple(node_to_matrix(node, R, C)) for node in the_cycle}
    # #print(the_cycle_coords)
    # #print(the_cycle, len(the_cycle))
    # CM = deepcopy(M)
    
    # sum_removed_elems = 0
    # for row_idx, row in tqdm(enumerate(M)):
    #     for col_idx, value in enumerate(row):
    #         if value != "." and ((row_idx, col_idx) not in the_cycle_coords):
    #             CM[row_idx][col_idx] = "#"
    #             sum_removed_elems += 1
                
    
    first = 13728 // 2            
    sl = 0
    loop_coords = [tuple(node_to_matrix(node, R, C)) for node in the_cycle]
    for idx, curr in enumerate(loop_coords):
        a = loop_coords[idx - 1]
        b = curr
        sl += (a[0] * b[1]) - (a[1] * b[0])

    print(sl)
    print(((sl - 13728) / 2) + 1)
    
        
        
    
    #for row_idx, row in enumerate(CM):
    #    print("".join(row), row_idx)
        
    # CMM = []
    # points = 0
    # for row_idx, row in enumerate(CM):
    #     line = "".join(row)
    #     replaced_line = list(line)
    
    #     for col_idx, value in enumerate(row):
    #         if value not in {".", "#"}:
    #             break
    #         replaced_line[col_idx] = "#"
            
    #     for col_idx, value in enumerate(row[::-1]):
    #         if value not in {".", "#"}:
    #             break
    #         replaced_line[140-col_idx-1] = "#"
    
                
    #     replaced_line = "".join(replaced_line)
                
    #     replaced_line = (
    #         replaced_line
    #         .replace("7", "┐")
    #         .replace("L", "└")
    #         .replace("F", "┌")
    #         .replace("J", "┘")
    #     )
        
    #     CMM.append(list(replaced_line))
    #     #print_colored_string(replaced_line)
    #     points += Counter(replaced_line)["."]
    # print(points)
                
    # in_count = False
    # for row_idx, row in enumerate(CM):
    #     for col_idx, value in enumerate(row):
    #         pass
            
    
    
    # states
    # 1: in loop -> COUNTING 
    # 0: out of loop -> NOT COUNTING


    # count_enclosed = 0
    
    # for row_idx, row in enumerate(M):
    
    #     print("row", row_idx)
    #     count_of_in_cycle_chars = 0
    #     state = 0

    #     for col_idx, value in enumerate(row): 
    
    #         if (state == 0) and (value in {"S", "F", "7", "L", "J", "|"}):
    #             state = 1
    #             print("state to 1")
    #         elif (state == 1) and (value in {"S", "F", "7", "L", "J", "|"}):
    #             state = 0
    #         elif (state == 1) and (value == "-"):
    #             print("-, state still 1")
                
                
    #         if value != "." and matrix_to_node(row_idx, col_idx, R) in set(G.nodes): # set(G.nodes)
    #             count_of_in_cycle_chars += 1
                
    #         print(row_idx, col_idx, value, state, count_enclosed, count_of_in_cycle_chars)

    #         row_char_counts = Counter(row)
            
    #         # (count_of_in_cycle_chars - row_char_counts["-"] - row_char_counts["|"]) % 2 == 0:
    #         if (state == 1) and (value == "."):
    #             print(row_idx, col_idx, count_of_in_cycle_chars, "COUNTING!+!!!")
    #             count_enclosed += 1
    #     count_of_in_cycle_chars = 0
       
            
    # print(count_enclosed)
            
                    
            
        
        
    # node_coords = []
    # if the_cycle:
    #     for node in the_cycle:
    #         node_coords.append(node_to_matrix(node, R, C))
    

    # print(node_coords)
    

            
if __name__ == "__main__":
    data = Path("day10.input").read_text().strip()
    
    example_1 = """
.....
.S-7.
.|.|.
.L-J.
.....
    """
    
#     example_1 = """
# .....
# .S-7.
# ...J.
# .....
# .....
#     """
    
    example_2 = """
    ..F7.
.FJ|.
SJ.L7
|F--J
LJ...
    """
    
    example_second = """
    
    ...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
    """
    
    example_second_2 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
    """
    #287 - 430
    
    #second(example_second_2)
    second(data)