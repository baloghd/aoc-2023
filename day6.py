import re
from collections import defaultdict
from functools import reduce
from pathlib import Path

from tqdm import tqdm


def parse_input(input):
    times, distances = [], []
    for idx, line in enumerate(input.strip().split("\n")):
        if line.startswith("Time"):
            times = [int(x) for x in line.split(":")[1].strip().split(" ") if x != ""]
        elif line.startswith("Dist"):
            distances = [int(x) for x in line.split(":")[1].strip().split(" ") if x != ""]
    return times, distances
    

def ways(t: int, d: int, filter_bads: bool = True):
    distances = []
    for press_duration in tqdm(range(t)):
        distance = press_duration * (t - press_duration) 
        if filter_bads:
            if distance > d:
                distances.append((press_duration, distance))
        else:
            distances.append((press_duration, distance))
    return distances

def ways_optimized(t: int, d: int, filter_bads: bool = True):
    count_when_distances_exceed = 0
    for press_duration in tqdm(range(1, t)):
        distance = press_duration * (t - press_duration) 
        if filter_bads:
            if distance > d:
                count_when_distances_exceed += 1
                #distances.append((press_duration, distance))
    return count_when_distances_exceed
        


def first(input):
    t, d = parse_input(input)
    print(t)
    print(d)
    
    q = 1
    
    for time, distance in zip(t, d):
        #w = ways(time, distance)
        #q *= len(w)
        q *= ways_optimized(time, distance, 1)
    print(q)
        
        
def second(input):
    for idx, line in enumerate(input.strip().split("\n")):
        print(line)
            
if __name__ == "__main__":
    data = Path("day6.input").read_text().strip()
    
    example = """
    Time:      7  15   30
Distance:  9  40  200   
    """
    
    example2 = """
    Time:      71530
Distance:  940200   
    """
    first(data)