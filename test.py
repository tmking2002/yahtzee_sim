import yahtzee
import matplotlib.pyplot as plt
import numpy as np

blank_scorecard = {
        "ones": None,
        "twos": None,
        "threes": None,
        "fours": None,
        "fives": 5,
        "sixes": None,
        "three_of_a_kind": None,
        "four_of_a_kind": None,
        "full_house": None,
        "small_straight": None,
        "large_straight": None,
        "yahtzee": None,
        "yahtzee_bonus_1": None,
        "yahtzee_bonus_2": None,
        "yahtzee_bonus_3": None,
        "chance": None
    }

#yahtzee.sim_games(1, "upper_bonus", True)
#dice = [5, 5, 5, 3, 3]
#print(yahtzee.decide_dice(dice, 1, blank_scorecard, "upper_bonus"))
#print(yahtzee.get_scores(dice, blank_scorecard))
#print(yahtzee.decide_score(scorecard = blank_scorecard, possible_scores = yahtzee.get_scores(dice, blank_scorecard), strategy = "upper_bonus"))