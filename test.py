import yahtzee

blank_scorecard = {
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
        "yahtzee_bonus_1": None,
        "yahtzee_bonus_2": None,
        "yahtzee_bonus_3": None,
        "chance": None
    }

yahtzee.sim_games(1, "upper_bonus", True)
#dice = [2, 4, 5, 3, 3]
#print(yahtzee.get_scores(dice, blank_scorecard))