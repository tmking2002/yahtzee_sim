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

def decide_dice(dice, turn_num, scorecard):
    most_common = max(set(dice), key=dice.count)
    kept_dice = [x for x in dice if x == most_common]

    return kept_dice

def decide_score(scorecard, possible_scores):
    sorted_scores = sorted(possible_scores, key=possible_scores.get, reverse=True)

    for score in sorted_scores:
        if scorecard[score] is None:
            return score
        
def turn(scorecard):
    dice = roll_dice(5) 
    kept_dice = decide_dice(dice, 1, scorecard)

    dice = kept_dice + roll_dice(5 - len(kept_dice))
    kept_dice = decide_dice(dice, 2, scorecard)

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
        "yahtzee_bonus_1": None,
        "yahtzee_bonus_2": None,
        "yahtzee_bonus_3": None,
        "chance": None
    }

    while None in [value for key, value in scorecard.items() if key not in ["yahtzee_bonus_1", "yahtzee_bonus_2", "yahtzee_bonus_3"]]:
        dice = turn(scorecard)
        possible_scores = get_scores(dice, scorecard)

        score = decide_score(scorecard, possible_scores)
        scorecard[score] = possible_scores[score]

    upper_total = sum(scorecard[score] for score in ["ones", "twos", "threes", "fours", "fives", "sixes"])
    upper_bonus = 35 if upper_total >= 63 else 0

    # add upper bonus to scorecard
    scorecard["upper_bonus"] = upper_bonus
    total_score = sum(filter(None, scorecard.values())) + upper_bonus

    #st.dataframe(scorecard, width=1000, height = 520)
    #st.write("Total Score: ", total_score)

    return(total_score, scorecard)

def sim_games(n):
    start_time = time.time()    
    scores = []
    max_score = 0
    for i in range(n):
        score, scorecard = game()
        scores.append(score)
        if score > max_score:
            max_score = score
            best_scorecard = scorecard
    end_time = time.time()
    st.write("Time: ", f"{round(end_time - start_time, 4)}", "seconds")
    return scores, best_scorecard

st.set_option('deprecation.showPyplotGlobalUse', False)

# Main Streamlit code
n = st.number_input("Number of games to simulate", 1, 100000, 1000)
if st.button("Start"):
    scores, best_scorecard = sim_games(n)
    st.write("Average Score: ", sum(scores) / len(scores))
    st.write("Median Score", sorted(scores)[len(scores) // 2])
    st.write("Max Score: ", max(scores))
    plt.hist(scores, bins=range(0, 600, 10))
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    st.pyplot()
    st.dataframe(best_scorecard, width=1000, height = 600)
    st.write("Total Score: ", sum(filter(None, best_scorecard.values())))



