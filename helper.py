import numpy as np
import pandas as pd
from tqdm import tqdm

def create_all_comb(num_colors=6, num_actions=4):
    pos = pd.DataFrame({
        'c': range(6),
        'key': 1
    })
    all_comb = pos
    for i in range(4-1):
        all_comb = all_comb.merge(pos, how='outer', on='key', suffixes=('_x'+str(i), '_y'+str(i)))
    all_comb = all_comb.drop('key', axis=1)
    all_comb.columns = range(4)
    return np.array(all_comb)

def scoring(guess, true, num_actions=4):
    R, W = 0, 0

    # hashmap: storing the true value w.r.t. its occurance
    true_hash = {}
    for i in range(num_actions):
        if true[i] in true_hash:
            true_hash[true[i]] += 1
        else:
            true_hash[true[i]] = 1

    # avoid duplicated guessing
    # e.g. true = [4,3,2,3]; guess = [1,3,0,5]
    # count num red
    guessed = []
    for i in range(num_actions):
        if guess[i] == true[i]:
            R += 1
            true_hash[true[i]] -= 1
            guessed.append(i)
    # count num white
    for i in range(num_actions):
        if guess[i] in true_hash and true_hash[guess[i]] > 0 and not i in guessed:
            W += 1
            true_hash[guess[i]] -= 1

    return R, W

def make_score_table(guesses, possible_comb):
    score_table = {}
    for i, guess in tqdm(enumerate(guesses)):
        res = []
        for true in possible_comb:
            res.append(scoring(guess, true))
        score_table[i] = res
    score_table = pd.DataFrame(score_table)
    return score_table