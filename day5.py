import re
from collections import defaultdict
from functools import reduce
from itertools import pairwise
from pathlib import Path

from tqdm import tqdm


def parse(line, parsed_maps, mapname):
    if ":" in line:
        line = line.split(":")
        if line[0] == "seeds":
            parsed_maps["seeds"] = [int(x) for x in line[1].strip().split()]
        if "map" in line[0]:
            mapname = re.match(r"(.*) map", line[0]).groups()[0]
            print(f"{mapname} changed")
            if mapname not in parsed_maps:
                parsed_maps[mapname] = []
    else:
        #if mapname:
        if line.split(" ")[0] != '':
            numbers = [int(x) for x in line.split(" ")]
            #print(numbers, mapname)
            parsed_maps[mapname].append(numbers)
            #print(line.split(" "))
    return mapname
       
            
def translate(number, list_of_mappings):
    
    number_needs_translation = False
    for dest, source, _range in list_of_mappings:
        if number >= source and number <= source + _range - 1:
            translated = number - source + dest
            return translated
    return number
        
    
def translate_smart(number, list_of_mappings):
    pass    


def first(input):
    parsed_maps = {}
    mapname = None
    for idx, line in enumerate(input.strip().split("\n")):
        mapname = parse(line, parsed_maps=parsed_maps, mapname=mapname)
    print(parsed_maps)
    
    #translator_map = {"seed": parsed_maps["seeds"]}
    #seeds_to_check=[(1416733839, 1482960020), (2082912089, 2087629380), (4076319163, 4078486540), (4101717262, 4134687099)]
    translator_map = {"seed": [4134687099]}
    print(translator_map)
    for key in parsed_maps:
        if key != "seeds":
            print(key)
            _from, _, _to = key.split("-")
            translator_map[_to] = []
            for source in translator_map[_from]:
                t = translate(source, parsed_maps[key])
                print(source, parsed_maps[key], t)
                translator_map[_to].append(t)
            print(translator_map)
    print(min(translator_map["location"]))
            

def sort_by_dest(list_of_mappings):
    return sorted(list_of_mappings, key=lambda x: x[0])

def fill_and_add_min_range(list_of_mappings):
    sorted_lom_by_dest = sort_by_dest(list_of_mappings)
    
    first_dest, first_source, first_range = sorted_lom_by_dest[0]
    
    max_of_ranges = sorted_lom_by_dest[-1][0] + sorted_lom_by_dest[-1][2]
    print(f"{max_of_ranges=}")
    if first_dest > 0:
        min_range = [0, 0, first_dest]
        print(f"added {min_range=}")
        sorted_lom_by_dest = [min_range] + sorted_lom_by_dest
    
    fills = []
    
    for a, b in pairwise(sorted_lom_by_dest):
        #print(a, " -> ", b)
        max_dest_of_current_range = a[0] + a[2]
        start_dest_of_next = b[0]
        if max_dest_of_current_range != start_dest_of_next:
            gap_length = start_dest_of_next - max_dest_of_current_range
            #print(f"GAP of length {gap_length}")
            fills.append([max_dest_of_current_range, max_dest_of_current_range + gap_length, gap_length])
            #print(fills)
    
    fills.append([max_of_ranges, max_of_ranges, 1_000_000_000_000_000_000])
    
    return sort_by_dest(sorted_lom_by_dest + fills)
        
        
def findoverlap(s1,e1,s2,e2):
    
    if max(s1, s2) > min(e1, e2):
        #print("no overlap")
        return (None, None)
    
    start, end = max(s1, s2), min(e1, e2)
    return (start, end) 

def parse_filled_segments(source: str, dest: str, list_of_mappings):
    parsed = []
    for _dest, _source, _length in list_of_mappings:
        parsed.append({
            "source": source,
            "source_range": [_source, _source + _length - 1],
            "dest": dest,
            "dest_range": [_dest, _dest + _length - 1],
            
     
            
            "delta":  _dest - _source
        })
    return parsed

def seed_to_seed_segments(seeds):
    i = 0
    seed_segments = []
    while i < len(seeds):
        seed_segments.append([seeds[i], seeds[i] + seeds[i+1]])
        i += 2
    return seed_segments

def find_overlap_of_seeds_and_segments(seed, needed_range_segments):
    ols = []
    for s in seed:
        for n in needed_range_segments:
            ol = findoverlap(*s, *n)
            #print(s, n, ol)
            if ol[0] is not None:
                ols.append(ol)
    return ols


def second(input):
    parsed_maps = {}
    mapname = None
    for idx, line in enumerate(input.strip().split("\n")):
        mapname = parse(line, parsed_maps=parsed_maps, mapname=mapname)
    #print(parsed_maps)
    p = parsed_maps
    #print(parsed_maps["seeds"])
    
    backprop = ['humidity-to-location',
                'temperature-to-humidity',
                'light-to-temperature',
                'water-to-light',
                'fertilizer-to-water',
                'soil-to-fertilizer',
                'seed-to-soil']
    
    
    print("*"*50, "FIRST ITERATION STARTS", "*"*50)

    b = backprop[0]
    print(f"source -> {b} <- dest")
    _from, _, _to = b.split("-")
    filled_p_of_b = fill_and_add_min_range(p[b])
    parsed_filled_p_of_b = parse_filled_segments(source=_from, dest=_to, list_of_mappings=filled_p_of_b)

    print(f"{parsed_filled_p_of_b=}")
    first_dest_segment = parsed_filled_p_of_b[0]
    needed_range_segments = [first_dest_segment['source_range']]
    print(f"{first_dest_segment=}")
    print(f"{needed_range_segments=} FOR {_from}")
    print("*"*50, "FIRST ITERATION OVER", "*"*50)

    
    for b in backprop[1:]:
        print(f"source -> {b} <- dest")
        print(p[b])
        _source, _, _dest= b.split("-")
        filled_p_of_b = fill_and_add_min_range(p[b])
        parsed_filled_p_of_b = parse_filled_segments(source=_source, dest=_dest, list_of_mappings=filled_p_of_b)
        print(f"{parsed_filled_p_of_b=}")
    
        updated_needed_range_segments = []
        
        for segment in needed_range_segments:
            for mapping_segment in parsed_filled_p_of_b:
                print(f"{_dest} {segment=}, {_source} {mapping_segment['source_range']=}")
                source_segment_start, source_segment_end = mapping_segment['source_range']
                delta = mapping_segment["delta"]
                #print(f" finding overlaps with {segment[0], segment[1], mapping_segment[0], mapping_segment[0] + mapping_segment[2]}")
                overlap_start, overlap_end = findoverlap(segment[0], segment[1], source_segment_start+delta, source_segment_end+delta)
                #if overlap_start:
                print(f"--------------------- overlap found: {overlap_start, overlap_end}") 
                if overlap_start is not None:
                    updated_needed_range_segments.append([overlap_start, overlap_end])
        print(f"{updated_needed_range_segments=}")
        needed_range_segments = updated_needed_range_segments
        
        print("#"*50)
        
    
    seed_segments = seed_to_seed_segments(p['seeds'])
    seeds_to_check = find_overlap_of_seeds_and_segments(seed_segments, needed_range_segments)
    print(seeds_to_check)
    
    all_seeds = set()
    for start, end in seeds_to_check:
        for s in range(start, end+1):
            #print(f"adding {s=}")
            all_seeds.add(s)
    #print(all_seeds)
        
    # list(range(735979771, 737907828+1))
            
    translator_map = {"seed": list(all_seeds)}
    #print(translator_map)
    for key in parsed_maps:
        if key != "seeds":
            #print(key)
            _from, _, _to = key.split("-")
            translator_map[_to] = []
            for source in translator_map[_from]:
                t = translate(source, parsed_maps[key])
                #print(source, parsed_maps[key], t)
                translator_map[_to].append(t)
            #print(translator_map)
    v = min(translator_map["location"])
    print("Seed: ", translator_map["seed"][translator_map['location'].index(v)])
    print(f"value={v}")
    
    
    
    
    
    
    
from collections import namedtuple

RangeMapping = namedtuple("RangeMapping", ["dest", "source", "range", "delta"], defaults=[None for _ in range(4)])

def sort_by_dest_rm(list_of_range_mappings):
    return sorted(list_of_range_mappings, key=lambda x: x.dest)

        
def fill_range_mappings(list_of_range_mappings):
    sorted_rm_list = sort_by_dest_rm(list_of_range_mappings)
    lowest_rm_in_list = sorted_rm_list[0]
    highest_rm_in_list = sorted_rm_list[-1]
    
    # add zero RM if not present
    if lowest_rm_in_list.dest > 0:
        zero_delta_rm = RangeMapping(dest=0, source=0, range=lowest_rm_in_list.dest, delta=0)
        sorted_rm_list = [zero_delta_rm] + sorted_rm_list
        
    
    # add batárnagy RM
    sorted_rm_list += [RangeMapping(
        dest=highest_rm_in_list.dest + highest_rm_in_list.range,
        source=highest_rm_in_list.dest + highest_rm_in_list.range,
        range=1_000_000_000_000,
        delta=0
    )]     
    
    gapfills = []
    
    # fill gaps
    for a, b in pairwise(sorted_rm_list):
        if a.dest + a.range < b.dest:
            print("GAP")
            gapfiller = RangeMapping(dest=a.dest + a.range + 1, source=a.dest + a.range + 1, range=b.dest - a.dest + a.range, delta=0)
            gapfills.append(gapfiller)
            print(gapfiller)
    
    return sort_by_dest_rm(sorted_rm_list + gapfills)
    

def second_new(input):
    parsed_maps = {}
    mapname = None
    for idx, line in enumerate(input.strip().split("\n")):
        mapname = parse(line, parsed_maps=parsed_maps, mapname=mapname)
    
    print(parsed_maps)
    
    range_mappings = defaultdict(list)

    for key in parsed_maps:
        if key != "seeds":
            for obj in parsed_maps[key]:
                rm = RangeMapping(*obj, obj[0] - obj[1]) # delta = dest - source
                range_mappings[key].append(rm)
                
    print(range_mappings)
    
    backprop = ['humidity-to-location',
                'temperature-to-humidity',
                'light-to-temperature',
                'water-to-light',
                'fertilizer-to-water',
                'soil-to-fertilizer',
                'seed-to-soil']
    
    for key in range_mappings:
        range_mappings[key] = fill_range_mappings(range_mappings[key])
        print("*" * 50, key, "*"* 50)
        print(range_mappings[key])
    print("#"*80)
    print("#"*30, "FIRST ITERATION", "#"*30)
    transition = backprop[0]
    _source, _, _dest = transition.split("-")
    print(transition)
    print(range_mappings[transition])
    
    location_target_range = range_mappings[transition][1]
    print(f"{_dest=}", range_mapping_to_range(location_target_range, side="dest"))
    print(f"{_source=}", range_mapping_to_range(location_target_range, side="source"))
    
    ranges_of_current_source = [range_mapping_to_range(location_target_range, side="source")]
    dest_target_ranges = None
    print(f"{_source}, {ranges_of_current_source=}")
    
    for transition in backprop[1:]:
        _source, _, _dest = transition.split("-")
        print("*" * 50, transition, "*"* 50)
        print(range_mappings[transition])
    
        dest_target_ranges = ranges_of_current_source
        print(f"{_dest=}", f"{dest_target_ranges=}")
                
        ranges_of_current_source = []
        for rm in range_mappings[transition]:
            for target_range in dest_target_ranges:
                print(rm, target_range, rm.dest, rm.dest + rm.range + 1)
                # find overlap 
                o_start, o_end = findoverlap(*target_range, rm.dest, rm.dest + rm.range + 1)
                if o_start is not None:
                    print(o_start-rm.delta, o_end-rm.delta)
                    ranges_of_current_source.append([o_start-rm.delta, o_end-rm.delta])
        print(f"{_source=}, {ranges_of_current_source=}")
    
    seed_segments = sorted(seed_to_seed_segments(parsed_maps['seeds']), key=lambda x: x[0])
    print(f"{seed_segments=}")
    for segment in seed_segments:
        for range_source_segment in ranges_of_current_source:
            o_s, o_e = findoverlap(*segment, *range_source_segment)
            if o_s is not None:
                print(o_s, o_e)
    seeds_to_check = find_overlap_of_seeds_and_segments(seed_segments, ranges_of_current_source)
    
    print(f"{seeds_to_check=}")
    
    all_seeds = set()
    for start, end in seeds_to_check:
        for s in range(start, end+1):
            #print(f"adding {s=}")
            all_seeds.add(s)
    #print(all_seeds)
        
    translator_map = {"seed": list(all_seeds)}
    #print(translator_map)
    for key in parsed_maps:
        if key != "seeds":
            #print(key)
            _from, _, _to = key.split("-")
            translator_map[_to] = []
            for source in tqdm(translator_map[_from]):
                t = translate(source, parsed_maps[key])
                #print(source, parsed_maps[key], t)
                translator_map[_to].append(t)
            #print(translator_map)
    v = min(translator_map["location"])
    print(len(translator_map["location"]))
    print("Seed: ", translator_map["seed"][translator_map['location'].index(v)])
    print(f"value={v}")
    return v
        
    
    
    
def range_mapping_to_range(rm: RangeMapping, side: str = "source"):
    if side == "dest":
        return [rm.dest, rm.dest + rm.range - 1]
    elif side == "source":
        return [rm.source, rm.source + rm.range - 1]
    


    

if __name__ == "__main__":
    data = Path("day5.input").read_text().strip()
    # 79 14 55 13
    example = """
    seeds:  79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    """
   
    Seed:  4122758665
    value=2283878038
    too high
     
    Seed:  1261955430
    value=923350392 
    too high
    """

    first(data)
    
    #assert second_new(example) == 46
    #second_new(data)