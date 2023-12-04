
import re
from collections import defaultdict
from functools import reduce
from pathlib import Path


def parse_card(line):
    card, numbers = line.split(":")
    card_id = int(re.search("([0-9].*)", card).groups()[0])
    win, have = numbers.split("|")
    
    win = {int(w) for w in win.strip().split(" ") if w.isnumeric()}
    have = {int(h) for h in have.strip().split(" ") if h.isnumeric()}

    return {"id": card_id, "win": win, "have": have}

def points_calc(win, have):
    print(win.intersection(have))
    common = win.intersection(have)
    if len(common) > 0:
        print(2**(len(common) - 1))
        return 2**(len(common) - 1)
    else:
        return 0
    
def num_of_winning(win, have):
    common = win.intersection(have)
    return len(common)

def first(input):
    sum_points = 0
    for idx, line in enumerate(input.strip().split("\n")):
        print(line)
        card = parse_card(line)
        points = points_calc(card["win"], card["have"])
        sum_points += points
    print(sum_points)
        
        
def second(input):
    
    card_win_map = {}
    cards = defaultdict(list)

    for idx, line in enumerate(input.strip().split("\n")):
        card = parse_card(line)
        print(card)
        card_win_map[card['id']] = num_of_winning(card['win'], card['have'])
        cards[card['id']].append(card)
        
    print (card_win_map)      
    #print(cards)
    
    numcards = len(card_win_map)
    for card_id, card_list in cards.items():
        number_of_cards_made = card_win_map[card_id]
        for maker_card in card_list:
            for delta in range(1, number_of_cards_made + 1):
                cards[card_id + delta].append(cards[card_id + delta][0])
            
    v = cards.values()
    #print(list(map(len, v)))
    print(sum(list(map(len, v))))
    
        
        
if __name__ == "__main__":
    data = Path("day4.input").read_text().strip()
  
    example = """
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """
    #first(data)
    second(data)
    
# {1: 5, 2: 0, 3: 5, 4: 2, 5: 0, 6: 2, 7: 1, 8: 1, 9: 0, 0: 8}