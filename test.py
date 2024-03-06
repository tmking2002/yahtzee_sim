from yahtzee import decide_dice

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

print(decide_dice([2, 2, 1, 5, 5], turn_num=1, scorecard=blank_scorecard, strategy="most_common"))