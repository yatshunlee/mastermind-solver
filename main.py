import numpy as np
import pandas as pd
from helper import *

if __name__ == '__main__':
    all_comb = create_all_comb()
    guesses = create_all_comb()

    while True:
        true = input('What is your secret code (type q to leave)? ')
        if true == 'q':
            print('Bye~~')
            break
        possible_comb = all_comb    
        true = np.array(eval(f"[{true}]"))
        while True:
            score_table = make_score_table(guesses, possible_comb)
            entropies = []
            for i in score_table.columns:
                entropies.append(score_table[i].value_counts(
                    normalize=True).apply(
                    lambda p: - p * np.log2(p)).sum())
            action = guesses[np.argmax(entropies)]
            res = scoring(action, true)
            print('AI chooses:', action, 'and gets a result:', res)
            possible_comb = possible_comb[
                score_table[score_table[np.argmax(entropies)]==res
            ].index]
            if possible_comb.shape[0] == 1:
                print('AI guesses', possible_comb[0], 'as the final answer.')
                break