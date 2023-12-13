import re
from collections import Counter
from functools import cache, reduce
from itertools import permutations
from multiprocessing import Pool
from pathlib import Path

from tqdm import tqdm

# def wildcards(s):
#     w = set()
#     for idx, c in enumerate(s):
#         if c == "?":
#             w.add(idx)
#     return w

@cache
def get_layout(s):
    return [len(x) for x in s.split(".") if x != ""]


def generate_strings(s, ht_to_gen):
    #@cache
    def recur(index, current_string, agh, ht_to_gen):
        if (index == len(s)):
            if agh == ht_to_gen:
                result.append(current_string)
                return
            else:
                return

        if s[index] == '?':
            recur(index + 1, current_string + '.', agh, ht_to_gen)
            recur(index + 1, current_string + '#', agh + 1, ht_to_gen)
        else:
            recur(index + 1, current_string + s[index], agh, ht_to_gen)

    result = []
    recur(0, '', agh=0, ht_to_gen=ht_to_gen)
    return result

# def input_wildcards(arr, w, perm):
#     arrlist = list(arr)
#     for wildcard_pos, perm_elem in zip(w, perm):
#         arrlist[wildcard_pos] = perm_elem
#     return "".join(arrlist)




# def arr_to_len_ops(line):
#     arr, layout = line.split(" ")
#     c = Counter(line)["?"]
#     layout = [int(x) for x in layout.split(",") if x != ""]
#     w = wildcards(arr)
    
#     n_hashtags = Counter(arr)["#"]
#     n_missing_hashtags = sum(layout) - n_hashtags
#     n_points_in_wildcards = len(w) - n_missing_hashtags

    
#     good_arrs = set()
#     seen_permutes = set()
    
    
#     missings = list("." * n_points_in_wildcards + "#" * n_missing_hashtags)

#     for p in permutations(missings):
#         if p in seen_permutes:
#             continue
#         seen_permutes.add(p)
#         candidate = input_wildcards(arr, w, p)
#         if get_layout(candidate) == layout:
#             good_arrs.add(candidate)
#     print(f"{line} done -> {c}")
#     return len(good_arrs)

def first(input):
    
    _sum = 0
    lines = []
    for idx, line in enumerate(input.strip().split("\n")):
        lines.append(line)
        
    lines = sorted(lines, key=lambda x: Counter(x)["?"])
    # pool = Pool(4)
    # res = pool.map(arr_to_len_ops, lines)
    
    for line in tqdm(lines):
        #print(line)
        arr, layout = line.split(" ")
        layout = [int(x) for x in layout.split(",") if x != ""]
    
        n_hashtags = Counter(arr)["#"]
        n_missing_hashtags = sum(layout) - n_hashtags

        perms = generate_strings(arr, n_missing_hashtags)
        
        _sum += len([p for p in perms if get_layout(p) == layout])
    print(_sum)
        
def unfold_line(line):
    arr, layout = line.split(" ")
    layout = [int(x) for x in layout.split(",") if x != ""]
    
    layout = layout * 5
    return "".join(list((list(arr) + ["?"])* 5)), layout 
        
        
def second(input):
   
    _sum = 0
    lines = []
    for idx, line in enumerate(input.strip().split("\n")):
        lines.append(line)
        
    lines = sorted(lines, key=lambda x: Counter(x)["?"])
    # pool = Pool(4)
    # res = pool.map(arr_to_len_ops, lines)
    
    for line in tqdm(lines):
        #print(line)
        print(line)

        arr, layout = unfold_line(line)
        print(arr, layout)
        n_hashtags = Counter(arr)["#"]
        n_missing_hashtags = sum(layout) - n_hashtags

        perms = generate_strings(arr, n_missing_hashtags)
        l = len([p for p in perms if get_layout(p) == layout])
        _sum += l
        print(l)
    print(_sum)
    
    
    
if __name__ == "__main__":
    data = Path("day12.input").read_text().strip()
    
    example = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
    """
    
    
    
    #first(data)
    second(data)