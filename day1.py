import re
from collections import defaultdict
from pathlib import Path
from typing import List

digit_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

def first(input):
    _sum = 0
    for line in input.split("\n"):
        match_digits = re.findall(r"\d", line)
        if match_digits:
            if len(match_digits) == 1:
                _sum += int(match_digits[0] + match_digits[0])  
            else:
                _sum += int(match_digits[0] + match_digits[-1])
    return _sum  


def line_to_digits(line: str) -> str:
    founds = defaultdict(int)
    for digit in digit_map:
        for find in re.finditer(f"({digit})", line):
            founds[find.start()] = digit

    for idx, digit in founds.items():
        tmp_line = list(line)
        tmp_line[idx] = str(digit_map[digit])
        line = "".join(tmp_line)
    
    return line


def second(input):
    _sum = 0
    for line in input.split("\n"):
        replaced = line_to_digits(line)
        match_digits = re.findall(r"\d", replaced)
        if match_digits:
            if len(match_digits) == 1:
                _sum += int(match_digits[0] + match_digits[0])  
            else:
                _sum += int(match_digits[0] + match_digits[-1])
    return _sum  
    
    
            
if __name__ == "__main__":
    data = Path("day1.input").read_text()
    #print(first(data))
    
    print(second("""two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    """))


    #line = "abcone2threexyz" 
    
        
    print(second(data))
            

    