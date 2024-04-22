from random import randint
import streamlit as st
import time
import matplotlib.pyplot as plt

max_scorecard = {
    "ones": 5,
    "twos": 10,
    "threes": 15,
    "fours": 20,
    "fives": 25,
    "sixes": 30,
    "three_of_a_kind": 30,
    "four_of_a_kind": 30,
    "full_house": 25,
    "small_straight": 30,
    "large_straight": 40,
    "yahtzee": 50,
    "yahtzee_bonus_1": 100,
    "yahtzee_bonus_2": 100,
    "yahtzee_bonus_3": 100,
    "chance": 30
}

def is_small_straight(dice):
    dice_set = set(dice)
    for i in range(1, 4):
        if set(range(i, i + 4)).issubset(dice_set):
            return True
    return False

def get_scores(dice, scorecard):
    scorecard = {
        "ones": dice.count(1),
        "twos": 2 * dice.count(2),
        "threes": 3 * dice.count(3),
        "fours": 4 * dice.count(4),
        "fives": 5 * dice.count(5),
        "sixes": 6 * dice.count(6),
        "three_of_a_kind": sum(dice) if any(dice.count(die) >= 3 for die in dice) else 0,
        "four_of_a_kind": sum(dice) if any(dice.count(die) >= 4 for die in dice) else 0,
        "full_house": 25 if len(set(dice)) == 2 and (dice.count(dice[0]) in [2, 3] or dice.count(dice[1]) in [2, 3]) else 0,
        "small_straight": 30 if is_small_straight(dice) else 0,
        "large_straight": 40 if [1, 2, 3, 4, 5] == sorted(dice) or [2, 3, 4, 5, 6] == sorted(dice) else 0,
        "yahtzee": 50 if len(set(dice)) == 1 else 0,
        "yahtzee_bonus_1": 100 if len(set(dice)) == 1 and scorecard['yahtzee'] == 50 else 0,
        "yahtzee_bonus_2": 100 if len(set(dice)) == 1 and scorecard['yahtzee'] == 50 and scorecard['yahtzee_bonus_1'] == 100 else 0,
        "yahtzee_bonus_3": 100 if len(set(dice)) == 1 and scorecard['yahtzee'] == 50 and scorecard['yahtzee_bonus_1'] == 100 and scorecard['yahtzee_bonus_2'] == 100 else 0,
        "chance": sum(dice)
    }
    return scorecard

def roll_dice(num_dice,):
    dice = [randint(1, 6) for _ in range(num_dice)]
    return dice

### Possible strategies
# 1. keep all dice: random
# 2. keep the most common: most_common
# 3. keeping the most common unless you have three in a row or more: check_straight
# 4. same as 3 but dont allow it to go for ones. also if score is below 10 then take 0 for 1s: no_ones
# 5. prioritize getting upper bonus: upper_bonus

def decide_dice(dice, turn_num, scorecard, strategy):

    if (len(set(dice)) == 2) & (max(dice.count(die) for die in dice) == 3) & (turn_num != 1) & (scorecard["full_house"] is None) & (sum(dice) < 22):
        return dice

    if strategy=="most_common":
        most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)

        kept_dice = [x for x in dice if x == most_common]
        
    elif strategy=="check_straight":

        straight_available = scorecard["small_straight"] is None or scorecard["large_straight"] is None

        if not straight_available:
            most_common = max(set(dice) - {1}, key=lambda x: (dice.count(x), x), default=0)
            kept_dice = [x for x in dice if x == most_common]
        else:
            possible_straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

            for straight in possible_straights:
                if all(die in dice for die in straight):
                    return straight
        
        most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)
        kept_dice = [x for x in dice if x == most_common]
                
        most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)
        kept_dice = [x for x in dice if x == most_common]
    
    elif strategy == "no_ones":

        straight_available = scorecard["small_straight"] is None or scorecard["large_straight"] is None

        if not straight_available:
            most_common = max(set(dice) - {1}, key=lambda x: (dice.count(x), x), default=0)
            kept_dice = [x for x in dice if x == most_common]
        else:
            possible_straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

            for straight in possible_straights:
                if all(die in dice for die in straight):
                    return straight
        
        most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)
        kept_dice = [x for x in dice if x == most_common]

    elif strategy=="upper_bonus":
        
        full_house_available = scorecard["full_house"] is None

        if full_house_available:
            if len(set(dice)) == 2:
                if max(dice.count(die) for die in dice) == 3:
                    return dice

        straight_available = scorecard["small_straight"] is None or scorecard["large_straight"] is None

        if (straight_available) & (([1, 2, 3, 4, 5] == sorted(dice)) | ([2, 3, 4, 5, 6] == sorted(dice))):
            return dice

        if not straight_available:
            most_common = max(set(dice) - {1}, key=lambda x: (dice.count(x), x), default=0)
            kept_dice = [x for x in dice if x == most_common]
        else:
            possible_straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
            possible_4_straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]

            if turn_num == 1:
                for straight in possible_straights:
                    if all(die in dice for die in straight):
                        return straight
            else:
                for straight in possible_4_straights:
                    if all(die in dice for die in straight):
                        return straight
            
            most_common = max(set(dice) - {1}, key=lambda x: (dice.count(x), x), default=0)
            second_most_common = max(set(dice) - {1, most_common}, key=lambda x: (dice.count(x), x), default=0)
            
            if (most_common == 0) & (second_most_common == 0):
                return dice

            lookup = {1: "ones", 2: "twos", 3: "threes", 4: "fours", 5: "fives", 6: "sixes"}

            # check for tie
            if dice.count(most_common) == dice.count(second_most_common):
                if (scorecard[lookup[most_common]] is not None) & (scorecard[lookup[second_most_common]] is None):
                    most_common = second_most_common

            kept_dice = [x for x in dice if x == most_common]


    elif strategy=="random":
        kept_dice = dice

    return kept_dice

def decide_score(scorecard, possible_scores, strategy, weights=None):
    sorted_scores = sorted(possible_scores, key=possible_scores.get, reverse=True)

    num_remaining_slots = len([value for key, value in scorecard.items() if value is None])

    if strategy == "no_ones":
        if possible_scores["ones"] is not None and max(possible_scores.values()) < 10:
            return "ones"
        
    elif strategy=="upper_bonus":

        weighted_scores = possible_scores.copy()

        if weights is not None:
            for key in weights:
                weighted_scores[key] *= weights[key]
        else:
            weighted_scores["ones"] *= 4
            weighted_scores["twos"] *= 1.4
            weighted_scores["threes"] *= 1.4
            weighted_scores["fours"] *= 1.3
            weighted_scores["fives"] *= 1.3
            weighted_scores["sixes"] *= 1.2

        weighted_scores["chance"] *= .25

        scores_minus_chance = {key: value for key, value in weighted_scores.items() if key != "chance"}

        if num_remaining_slots > 12:
            if max(scores_minus_chance.values()) > 10:
                weighted_scores["chance"] = 0
            if weighted_scores["sixes"] < 18:
                weighted_scores["sixes"] *= 0.2
            if weighted_scores["fives"] < 15:
                weighted_scores["fives"] *= 0.3
            if weighted_scores["fours"] < 12:
                weighted_scores["fours"] *= 0.4

        if (weighted_scores["three_of_a_kind"] < 15):
            weighted_scores["three_of_a_kind"] = 0
        if (weighted_scores["four_of_a_kind"] < 10):
            weighted_scores["four_of_a_kind"] = 0

        weighted_scores["four_of_a_kind"] += .1

        sorted_scores = sorted(possible_scores, key=weighted_scores.get, reverse=True)

        top_score = ""

        for score in sorted_scores:
            if scorecard[score] is None:
                top_score = score
                break

        # consider taking 0 on yahtzee in dire circumstances
        if (possible_scores[top_score] <= max_scorecard[top_score] * 0.2) & (scorecard["yahtzee"] is None):
            return "yahtzee"

    for score in sorted_scores:
        if scorecard[score] is None:
            return score
        
def turn(scorecard, strategy="most_common", debug=False):

    turn_num = len([value for key, value in scorecard.items() if value is not None]) + 1

    dice = roll_dice(5) 
    kept_dice = decide_dice(dice, 1, scorecard, strategy)
    if debug:
        st.write("**Turn:** ", turn_num, unsafe_allow_html=True)
        st.write("Dice: ", ', '.join(map(str, sorted(dice))))
        st.write("Kept Dice: ", ', '.join(map(str, sorted(kept_dice))))
        st.write("\n")

    dice = kept_dice + roll_dice(5 - len(kept_dice))
    kept_dice = decide_dice(dice, 2, scorecard, strategy)
    if debug:
        st.write("Dice: ", ', '.join(map(str, sorted(dice))))
        st.write("Kept Dice: ", ', '.join(map(str, sorted(kept_dice))))
        st.write("\n")

    dice = kept_dice + roll_dice(5 - len(kept_dice))
    if debug: 
        st.write("Dice: ", ', '.join(map(str, sorted(dice))))
        st.write("\n")

    return dice

def game(strategy="most_common", debug=False, weights=None):
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
        "yahtzee_bonus_1": None,
        "yahtzee_bonus_2": None,
        "yahtzee_bonus_3": None,
        "chance": None
    }

    while None in [value for key, value in scorecard.items() if key not in ["yahtzee_bonus_1", "yahtzee_bonus_2", "yahtzee_bonus_3"]]:
        dice = turn(scorecard, strategy, debug)
        possible_scores = get_scores(dice, scorecard)

        score = decide_score(scorecard, possible_scores, strategy, weights)
        if debug:
            st.write("Score: ", score)
            other_possible_scores = {key: value for key, value in possible_scores.items() if key != score and value > 0 and scorecard[key] is None}
            st.write("Possible Scores: ", other_possible_scores)
            print("\n")

        scorecard[score] = possible_scores[score]

    upper_total = sum(scorecard[score] for score in ["ones", "twos", "threes", "fours", "fives", "sixes"])
    upper_bonus = 35 if upper_total >= 63 else 0

    # add upper bonus to scorecard
    scorecard["upper_bonus"] = upper_bonus
    total_score = sum(filter(None, scorecard.values())) + upper_bonus

    return total_score, scorecard

def sim_games(n, strategy="most_common", debug=False, weights=None):
    start_time = time.time()    
    scorecards = []
    scores = []
    max_score = 0
    for i in range(n):
        score, scorecard = game(strategy, debug, weights)
        scores.append(score)
        if score > max_score:
            max_score = score
            best_scorecard = scorecard
        scorecards.append(scorecard)
    end_time = time.time()
    for scorecard in scorecards:
        for key in scorecard:
            if scorecard[key] is None:
                scorecard[key] = 0
    return scores, best_scorecard, scorecards, round(end_time - start_time, 4)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Main Streamlit code
st.sidebar.title("Yahtzee Simulator!!!")
n = st.sidebar.number_input("Number of games to simulate", 1, 100000, 1000)
strategy = st.sidebar.selectbox("Strategy", ["random", "most_common", "check_straight", "no_ones", "upper_bonus"])

hist, best_tab, average_tab, sample_game = st.tabs(["Score Distribution", "Best Scorecard", "Average Scorecard", "Sample Game"])

if st.sidebar.button("Start"):
    scores, best_scorecard, scorecards, time_taken = sim_games(n, strategy)
    st.sidebar.write("Time taken: ", time_taken, " seconds")
    st.sidebar.write("Average Score: ", sum(scores) / len(scores))
    st.sidebar.write("Median Score", sorted(scores)[len(scores) // 2])
    st.sidebar.write("Max Score: ", max(scores))
    with hist:
        plt.hist(scores, bins=range(0, 600, 10))
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        st.pyplot()
    with best_tab:
        st.write("Total Score: ", sum(filter(None, best_scorecard.values())))
        st.dataframe(best_scorecard, width=1000, height = 600)
    avg_scorecard = {}
    for key in best_scorecard:
        avg_scorecard[key] = sum([scorecard[key] for scorecard in scorecards]) / n
    with average_tab:
        st.dataframe(avg_scorecard, width=1000, height = 600)
    with sample_game:
        sample_scores, na, sample_scorecard, sample_time = sim_games(1, strategy, True)
        st.dataframe(sample_scorecard[0], width=1000, height = 600)
        st.write("Total Score: ", sum(filter(None, sample_scorecard[0].values())))



