import re
from collections import defaultdict
from functools import reduce
from itertools import cycle
from pathlib import Path


class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
        
    def __repr__(self):
        L = self.left.value if self.left else None
        R = self.right.value if self.right else None
        return f"Node {self.value} (L: {L}, R: {R})"
 

def first(input):
    
    instructions = []
    nodes = {}
    
    for idx, line in enumerate(input.strip().split("\n")):
        if {"L", "R"} == set(line):
            instructions = list(line)
        else:
            if "=" in line:
                parts = re.findall("(\w+)", line)
                if parts:
                    nodes[parts[0]] = Node(*parts)
               
            
        if line:
            print(line)
    
       
    for key, node in nodes.items():
        if node.value != nodes[node.left].value:
            node.left = nodes[node.left]
        else:
            node.left = None
            
        if node.value != nodes[node.right].value:
            node.right = nodes[node.right]
        else:
            node.right = None
        print(node)
    print(nodes)
    
    tree = nodes["AAA"]
    print(instructions)
    steps = 0
    print(tree)
    
    for inst in cycle(instructions):
        if tree.value == "ZZZ":
            break
        steps += 1
        if inst == "R":
            tree = tree.right
        elif inst == "L":
            tree = tree.left
            
        print(tree)
    print(steps)
    
def gcd(a, b):
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmm(*args):
    return reduce(lcm, args)

        
def second(input):
    instructions = []
    nodes = {}
    
    for idx, line in enumerate(input.strip().split("\n")):
        if {"L", "R"} == set(line):
            instructions = list(line)
        else:
            if "=" in line:
                parts = re.findall("(\w+)", line)
                if parts:
                    nodes[parts[0]] = Node(*parts)
               
            
        # if line:
        #     print(line)
            
    for key, node in nodes.items():
        if node.value != nodes[node.left].value:
            node.left = nodes[node.left]
        else:
            node.left = None
            
        if node.value != nodes[node.right].value:
            node.right = nodes[node.right]
        else:
            node.right = None
        # print(node)
    #print(nodes)
            
    current_nodes = [nodes[key] for key in nodes if key.endswith("A")]
    print(current_nodes)
    
    end_nodes = [nodes[key] for key in nodes if key.endswith("Z")]
    print(end_nodes)
    
    steps_numbers = []
    for i in range(len(current_nodes)):
        only_one_current_nodes = [current_nodes[i]]
        
        steps = 0
        for inst in cycle(instructions):
            if only_one_current_nodes[0].value.endswith("Z"):
                break
            # if all(node.value.endswith("Z") for node in only_one_current_nodes):
            #     break
            
            steps += 1
            for idx, tree in enumerate(only_one_current_nodes):
                if inst == "R":
                    only_one_current_nodes[idx] = tree.right
                elif inst == "L":
                    only_one_current_nodes[idx] = tree.left

            # if steps % 100000 == 0:
            #     print(steps, len([node for node in only_one_current_nodes if node.value.endswith("Z")]))
        print(steps)
        steps_numbers.append(steps)
    print(lcmm(*steps_numbers))
    
    
    
            
if __name__ == "__main__":
    data = Path("day8.input").read_text().strip()
    example = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
    """
    
    example2 = """
    RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)    
"""
    
    example_part2 = """
    LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
    """
    
    
    #second(example_part2)
    first(data)
    second(data)