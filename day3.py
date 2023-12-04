
import re
from collections import defaultdict
from functools import reduce
from pathlib import Path


def first(input):
    number_borders = defaultdict(list)
    symbol_coordinates = defaultdict(list)
    
    overlapping = {}
    
    for idx, line in enumerate(input.strip().split("\n")):
        row_length = len(line)
        print(idx)
        for find in re.finditer(r"(\d\d?\d?)", line):
            print(find)
            number_borders[idx].append(list(find.span()))
            overlapping[(idx, find.span())] = int(find.groups()[0])
        
        for find in re.finditer(r"[^0-9\.]", line):
            print(find)
            symbol_coordinates[idx].append(list(find.span())[0])

    print(number_borders)
    print(symbol_coordinates)
    print(overlapping)
    
    overlap_sum = 0
    
    for row, symbols in symbol_coordinates.items():
        for sym in symbols:
            y, x = row, sym
            print(row, x, input.strip().split("\n")[y][x])
            overlaps = check_row_for_overlaps(y, x, number_borders_for_row=number_borders) 
            print(overlaps)
            for overlap in overlaps:
                x, (_start, _end) = overlap
                
                if overlap in overlapping:
                    print(f"adding {overlap} = {overlapping[overlap]}")
                    overlap_sum += overlapping[overlap]
                    del overlapping[overlap]
            print("*"*50)
                    
    print(overlap_sum)
                


def between(x, a, b):
    if x >= a and x <= b:
        return True
    return



def check_row_for_overlaps(y, x, number_borders_for_row):
    
    overlaps = []
    
    if y - 1 in number_borders_for_row:
        print(f"checking row before: {y - 1}")
        for num in number_borders_for_row[y - 1]:
            num_start, num_end = num
            num_end -= 1
            for part in range(x-1, x+2):
                if between(part, num_start, num_end):
                    print(f"OVERLAP {part, num_start, num_end}")
                    overlaps.append((y - 1, (num_start, num_end+1)))
                    break
                #else:
                #    print(f"NO OVERLAP {x, num_start, num_end}")
                
    if y in number_borders_for_row:
        print("checking row")
        for num in number_borders_for_row[y]:
            num_start, num_end = num
            num_end -= 1
            for part in range(x-1, x+2):
                if between(part, num_start, num_end):
                    print(f"OVERLAP {part, num_start, num_end}")
                    overlaps.append((y, (num_start, num_end+1)))
                    break
                #else:
                #    print(f"NO OVERLAP {x, num_start, num_end}")
                
                
    if y + 1 in number_borders_for_row:
        print(f"checking row after: {y + 1}")
        for num in number_borders_for_row[y + 1]:
            num_start, num_end = num
            num_end -= 1
            for part in range(x-1, x+2):
                if between(part, num_start, num_end):
                    print(f"OVERLAP {part, num_start, num_end}")
                    overlaps.append((y + 1, (num_start, num_end+1)))
                    break
                #else:
                #    print(f"NO OVERLAP {x, num_start, num_end}")
                
   
    return overlaps
                
        
def second(input):
    number_borders = defaultdict(list)
    symbol_coordinates = defaultdict(list)
    
    overlapping = {}
    
    for idx, line in enumerate(input.strip().split("\n")):
        row_length = len(line)
        print(idx)
        for find in re.finditer(r"(\d\d?\d?)", line):
            print(find)
            number_borders[idx].append( list(find.span()))
            overlapping[(idx, find.span())] = int(find.groups()[0])
        
        for find in re.finditer(r"[^0-9\.]", line):
            print(find)
            symbol_coordinates[idx].append(list(find.span())[0])
    
    print(number_borders)
    print(symbol_coordinates)
    print(overlapping)
    
    gear_ratio_sum = 0
    
    for row, symbols in symbol_coordinates.items():
        for sym in symbols:
            y, x = row, sym
            symbol_char = input.strip().split("\n")[y][x]
            print(row, x, symbol_char)
            
            if symbol_char == "*":
                overlaps = check_row_for_overlaps(y, x, number_borders_for_row=number_borders) 
                print(overlaps)
                if len(overlaps) == 2:
                    first = overlapping[overlaps[0]]
                    second = overlapping[overlaps[1]]
                    print(first, second, first * second)
                    gear_ratio = first * second
                    gear_ratio_sum += gear_ratio

            print("*"*50)
    print(gear_ratio_sum)    

if __name__ == "__main__":
    data = Path("day3.input").read_text()
    example = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

    #first(data)
    second(data)

