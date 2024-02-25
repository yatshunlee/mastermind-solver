import numpy as np
import pandas as pd
from helper import *

if __name__ == '__main__':
    all_comb = create_all_comb()
    guesses = create_all_comb()

    while True:
        # ask user's input
        true = input(
            'What is your secret code (in the format of a, b, c, d with a range of (0 - 6))? You can type q to leave as well: ')
        # exit
        if true == 'q':
            print('Bye~~')
            break
        true = np.array(eval(f"[{true}]"))
        
        # check the true array
        if np.any(true < 0) or np.any(true >= 6):
            print('Invalid input.')
            continue

        possible_comb = all_comb
        while True:
            # get the look-ahead contingency table
            score_table = make_score_table(guesses, possible_comb)
            # calculate the entropies of each guess
            entropies = []
            for i in score_table.columns:
                entropies.append(score_table[i].value_counts(
                    normalize=True).apply(
                    lambda p: - p * np.log2(p)).sum())
            # make a guess with the largest entropy and check
            action = guesses[np.argmax(entropies)]
            res = scoring(action, true)
            print('AI chooses:', action, 'and gets a result:', res)
            # update the possible combinations table
            possible_comb = possible_comb[
                score_table[score_table[np.argmax(entropies)]==res
            ].index]
            # break the calculation loop if it remains only 1 possible combination
            if possible_comb.shape[0] == 1:
                print('AI guesses', possible_comb[0], 'as the final answer.')
                break
