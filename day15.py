import re
from collections import defaultdict
from functools import reduce
from pathlib import Path


def calc_hash(char, current_value=0):
    return ((ord(char)+current_value)*17)%256
    

def calc_string_hash(s):
    cv = 0
    for char in s:
        cv = calc_hash(char, cv)
    return cv

def first(input):
    _sum = 0
    for idx, line in enumerate(input.strip().split(",")):
        #print(line)
        cv = 0
        for char in line:
            cv = calc_hash(char, cv)
        #print(cv)
        _sum += cv
    print(_sum)
    
def second(input):
    boxes = defaultdict(list)
    for idx, line in enumerate(input.strip().split(",")):
        #print(line)
        if "=" in line:
            label, focal_length = line.split("=")
            b = boxes[calc_string_hash(label)]
            if len([l for l in b if l[0] == label]) > 0:
                boxes[calc_string_hash(label)] = [x if label != x[0] else (label, focal_length) for x in boxes[calc_string_hash(label)]]
            else:
                boxes[calc_string_hash(label)].append((label, focal_length))
        else:
            label = line[:-1]
            focal_length = None
            boxes[calc_string_hash(label)] = [x for x in boxes[calc_string_hash(label)] if x[0] != label]
        #print(boxes)
    #print(boxes)        
    _sum = 0
    for box_number, slots in boxes.items():
        for idx, slot in enumerate(slots):
            _sum += (box_number + 1) * (idx + 1) * int(slot[1])
    print(_sum)
        
        
            
if __name__ == "__main__":
    data = Path("day15.input").read_text().strip()
    example = """
    rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
    """
    # 
    first(data)
    second(data)