
from functools import reduce
from pathlib import Path


def process_game(line):
    line = line.strip().split(":")
    #print(line)
    plays = line[1].split(";")
    ret = {"id": int(line[0].split(" ")[1]), "plays": []}
    
    for play in plays:
        play_dict = {"red": 0, "green": 0, "blue": 0}
        for color in play.split(","):
            number, color_name = color.strip().split(" ")
            play_dict[color_name] = int(number)
        ret["plays"].append(play_dict)
        
    return ret


def first(input):
    
    """
    
    only 12 red cubes, 13 green cubes, and 14 blue cubes
    
    """
    possible_id_sum = 0
    for line in input.split("\n"):
        game = process_game(line)
        #print(game)
        possible = True
        for play in game["plays"]:
            if play.get("red") > 12 or play.get("green") > 13 or play.get("blue") > 14:
                #print("game is not possible")
                possible = False
        if possible:
            possible_id_sum += game['id']
    return possible_id_sum


def second(input):
    power_sum = 0
    for line in input.split("\n"):
        game = process_game(line)
        #print(game)
        max_counts = {"red": 0, "green": 0, "blue": 0}
        for play in game["plays"]:
            for color in play:
                max_counts[color] = max(max_counts[color], play[color])
        #print(max_counts)
        power = reduce(lambda x, y: x * y, max_counts.values())
        power_sum += power
        #print(f"min_set: {power}")
    return power_sum
            

if __name__ == "__main__":
    data = Path("day2.input").read_text()
    f = first(data)
    s = second(data)
    print(s)