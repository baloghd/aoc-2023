import functools
import re
from collections import Counter, defaultdict
from functools import reduce
from itertools import groupby
from pathlib import Path

strength = ["A", "K", "Q", "J", "T", 9, 8, 7, 6, 5, 4, 3, 2]
strength = list(map(str, strength))

strength_2 = ["A", "K", "Q", "T", 9, 8, 7, 6, 5, 4, 3, 2, "J"]
strength_2 = list(map(str, strength_2))

hand_type_order = [
    "five_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "three_of_a_kind",
    "two_pair",
    "one_pair",
    "high_card"
]

hand_type_mapped_order = {
    hand_type: idx for idx, hand_type in enumerate(hand_type_order)
}

def hand_counts(hand):
    return sorted(list(Counter(hand).values()))[::-1]

def get_strongest_card_in_hand(hand):
    for card in strength_2:
        if card in hand:
            return card


def five_of_a_kind(hand):
    return len(set(hand)) == 1

def four_of_a_kind(hand):
    return hand_counts(hand) == [4, 1]

def full_house(hand):
    return hand_counts(hand) == [3, 2] 

def three_of_a_kind(hand):
    return hand_counts(hand) == [3, 1, 1]

def two_pair(hand):
    return hand_counts(hand) == [2, 2, 1]

def one_pair(hand):
    return hand_counts(hand) == [2, 1,1,1]

def high_card(hand):
    return len(set(hand)) == 5


def get_hand_type(hand):
    for hand_func in hand_type_order:
        if globals()[hand_func](hand):
            return hand_func

def get_hand_type_with_jokers(hand):
    if "J" in hand:
        c = Counter(hand)
        
        number_of_Js = c.pop("J")
        if number_of_Js == 5:
            hand = "AAAAA"
        else:
        
            possible_hands = []
            for card in c:
                possible_hands.append(hand.replace("J", card))
            
            # strongest possible
            print(possible_hands)
            hand = sorted(possible_hands, key=lambda x: hand_type_mapped_order[get_hand_type(x)])[0]

    for hand_func in hand_type_order:
        if globals()[hand_func](hand):
            return hand_func



def order_same_hand_types(a, b): # two hands

    for a_card, b_card in zip(a[1], b[1]):
        if strength.index(a_card) < strength.index(b_card):
            return -1
        elif strength.index(a_card) > strength.index(b_card):
            return 1
    return 0
o_func = functools.cmp_to_key(order_same_hand_types)


def order_same_hand_types_jokers(a, b): # two hands

    for a_card, b_card in zip(a[1], b[1]):
        if strength_2.index(a_card) < strength_2.index(b_card):
            return -1
        elif strength_2.index(a_card) > strength_2.index(b_card):
            return 1
    return 0
o_func_jokers = functools.cmp_to_key(order_same_hand_types_jokers)

def first(input):
    hand_bet_map = {}
    
    for idx, line in enumerate(input.strip().split("\n")):
        hand, bet = line.split(" ")
        bet = int(bet)
        hand_bet_map[idx] = [hand, get_hand_type(hand), bet]

    sorted_by_hand_type = sorted(hand_bet_map, key=lambda x: hand_type_mapped_order[hand_bet_map[x][1]])
    #print()
    
    sorted_groups = []
    for group in groupby([[idx] + hand_bet_map[idx] for idx in sorted_by_hand_type], key=lambda x: x[2]):
        hands_in_group = [hand for hand in group[1]]
        print(group)
        print(sorted(hands_in_group, key=o_func))
        sorted_groups += sorted(hands_in_group, key=o_func)
        
    sorted_groups = sorted_groups[::-1]
    print(sorted_groups)
    winnings = 0
    for idx, hand in enumerate(sorted_groups):
        winnings += (idx + 1) * hand[-1]
        print((idx + 1) * hand[-1])
    print(winnings)
    
        
def second(input):
    hand_bet_map = {}
    
    for idx, line in enumerate(input.strip().split("\n")):
        hand, bet = line.split(" ")
        bet = int(bet)
        hand_bet_map[idx] = [hand, get_hand_type_with_jokers(hand), bet]
        
    sorted_by_hand_type = sorted(hand_bet_map, key=lambda x: hand_type_mapped_order[hand_bet_map[x][1]])
    print("*"*40)
    print(sorted_by_hand_type)
    print("*"*40)
    sorted_groups = []
    for group in groupby([[idx] + hand_bet_map[idx] for idx in sorted_by_hand_type], key=lambda x: x[2]):
        hands_in_group = [hand for hand in group[1]]
        print("#"*40)
        print(group)
        print(sorted(hands_in_group, key=o_func_jokers))
        print("#"*40)
        sorted_groups += sorted(hands_in_group, key=o_func_jokers)
        
    sorted_groups = sorted_groups[::-1]
    
    #print(sorted_groups)
    print("*"*40)
    winnings = 0
    for idx, hand in enumerate(sorted_groups):
        winnings += (idx + 1) * hand[-1]
        #print((idx + 1) * hand[-1])
    print(winnings)

            
if __name__ == "__main__":
    data = Path("day7.input").read_text().strip()
    example = """
    32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    """
    
   
    
    #first(data)
    " 251156055 too low"
    second(data)