import tkinter as tk
import time
from random import randint

def roll_dice(num_dice):
    return [randint(1, 6) for _ in range(num_dice)]

def decide(dice, turn_num):
    most_common = max(set(dice), key=dice.count)
    kept_dice = [x for x in dice if x == most_common]

    return kept_dice

def turn():
    dice = roll_dice(5) 
    kept_dice = decide(dice, 1)

    dice = kept_dice + roll_dice(5 - len(kept_dice))
    kept_dice = decide(dice, 2)

    dice = kept_dice + roll_dice(5 - len(kept_dice))

    return dice

def game():
    scorecard = {
        "ones": None,
        "twos": None,
        "threes": None,
        "fours": None,
        "fives": None,
        "sixes": None,
        "three_of_a_kind": None,
        "four_of_a_kind": None,
        "full_house": None,
        "small_straight": None,
        "large_straight": None,
        "yahtzee": None,
        "chance": None
    
    }

def main():
    kept_dice = turn()
    print("Kept dice:", kept_dice)

if __name__ == "__main__":
    main()
