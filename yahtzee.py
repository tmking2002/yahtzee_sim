from random import randint
import streamlit as st
import time
import matplotlib.pyplot as plt

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
        "small_straight": 30 if [1, 2, 3, 4] == sorted(dice[:4]) or [2, 3, 4, 5] == sorted(dice[1:5]) or [3, 4, 5, 6] == sorted(dice[2:6]) else 0,
        "large_straight": 40 if [1, 2, 3, 4, 5] == sorted(dice) or [2, 3, 4, 5, 6] == sorted(dice) else 0,
        "yahtzee": 50 if len(set(dice)) == 1 else 0,
        "yahtzee_bonus_1": 100 if len(set(dice)) == 1 and scorecard['yahtzee'] == 50 else 0,
        "yahtzee_bonus_2": 100 if len(set(dice)) == 1 and scorecard['yahtzee'] == 50 and scorecard['yahtzee_bonus_1'] == 100 else 0,
        "yahtzee_bonus_3": 100 if len(set(dice)) == 1 and scorecard['yahtzee'] == 50 and scorecard['yahtzee_bonus_1'] == 100 and scorecard['yahtzee_bonus_2'] == 100 else 0,
        "chance": sum(dice)
    }
    return scorecard

def roll_dice(num_dice):
    return [randint(1, 6) for _ in range(num_dice)]

### Possible strategies
# 1. keep all dice: random
# 2. keep the most common: most_common
# 3. keeping the most common unless you have three in a row or more: check_straight
# 4. same as 3 but dont allow it to go for ones. also if score is below 10 then take 0 for 1s: no_ones
# 5. prioritize getting upper bonus: upper_bonus

def decide_dice(dice, turn_num, scorecard, strategy):

    if strategy=="most_common":
        most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)

        kept_dice = [x for x in dice if x == most_common]
        
    elif strategy=="check_straight":

        straight_available = scorecard["small_straight"] is None or scorecard["large_straight"] is None

        if not straight_available:
            most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)
            kept_dice = [x for x in dice if x == most_common]
        else:
            possible_straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]

            for straight in possible_straights:
                if all(die in dice for die in straight):
                    return straight
                
        most_common = max(set(dice), key=lambda x: (dice.count(x), x), default=0)
        kept_dice = [x for x in dice if x == most_common]
    
    elif strategy in["no_ones", "upper_bonus"]:

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

    elif strategy=="random":
        kept_dice = dice

    return kept_dice

def decide_score(scorecard, possible_scores, strategy):
    sorted_scores = sorted(possible_scores, key=possible_scores.get, reverse=True)

    if strategy in ["no_ones", "upper_bonus"]:
        if possible_scores["ones"] is not None and max(possible_scores.values()) < 10:
            return "ones"
        
    elif strategy=="upper_bonus":
        weighted_scores = possible_scores.copy()

        weighted_scores["twos"] *= 2
        weighted_scores["threes"] *= 2
        weighted_scores["fours"] *= 1.5
        weighted_scores["fives"] *= 1.5
        weighted_scores["sixes"] *= 1.5

        #if weighted_scores["sixes"] >= 

        sorted_scores = sorted(weighted_scores, key=weighted_scores.get, reverse=True)

    for score in sorted_scores:
        if scorecard[score] is None:
            return score
        
def turn(scorecard, strategy="most_common"):
    dice = roll_dice(5) 
    kept_dice = decide_dice(dice, 1, scorecard, strategy)

    dice = kept_dice + roll_dice(5 - len(kept_dice))
    kept_dice = decide_dice(dice, 2, scorecard, strategy)

    dice = kept_dice + roll_dice(5 - len(kept_dice))

    return dice

def game(strategy="most_common"):
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
        dice = turn(scorecard, strategy)
        possible_scores = get_scores(dice, scorecard)

        score = decide_score(scorecard, possible_scores, strategy)

        scorecard[score] = possible_scores[score]

    upper_total = sum(scorecard[score] for score in ["ones", "twos", "threes", "fours", "fives", "sixes"])
    upper_bonus = 35 if upper_total >= 63 else 0

    # add upper bonus to scorecard
    scorecard["upper_bonus"] = upper_bonus
    total_score = sum(filter(None, scorecard.values())) + upper_bonus

    return(total_score, scorecard)

def sim_games(n, strategy="most_common"):
    start_time = time.time()    
    scorecards = []
    scores = []
    max_score = 0
    for i in range(n):
        score, scorecard = game(strategy)
        scores.append(score)
        if score > max_score:
            max_score = score
            best_scorecard = scorecard
        scorecards.append(scorecard)
    end_time = time.time()
    st.write("Time: ", f"{round(end_time - start_time, 4)}", "seconds")
    for scorecard in scorecards:
        for key in scorecard:
            if scorecard[key] is None:
                scorecard[key] = 0
    return scores, best_scorecard, scorecards

st.set_option('deprecation.showPyplotGlobalUse', False)

# Main Streamlit code
n = st.number_input("Number of games to simulate", 1, 100000, 1000)
strategy = st.selectbox("Strategy", ["random", "most_common", "check_straight", "no_ones", "upper_bonus"])

if st.button("Start"):
    scores, best_scorecard, scorecards = sim_games(n, strategy)
    st.write("Average Score: ", sum(scores) / len(scores))
    st.write("Median Score", sorted(scores)[len(scores) // 2])
    st.write("Max Score: ", max(scores))
    plt.hist(scores, bins=range(0, 600, 10))
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    st.pyplot()
    st.write("Best Scorecard")
    st.dataframe(best_scorecard, width=1000, height = 600)
    avg_scorecard = {}
    for key in best_scorecard:
        avg_scorecard[key] = sum([scorecard[key] for scorecard in scorecards]) / n
    st.write("Average Scorecard")
    st.dataframe(avg_scorecard, width=1000, height = 600)
    st.write("Total Score: ", sum(filter(None, best_scorecard.values())))



