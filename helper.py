import numpy as np
import pandas as pd
from tqdm import tqdm

def create_all_comb(num_colors=6, num_pegs=4):
    """
    :param: num_colors (int)
    :param: num_pegs (int)
    return an 2D array with 
        columns = p0 p1 p2 p3 (for num_pegs=4)
        rows = guess_id / combination_id
        value = color code in the peg
    """
    pos = pd.DataFrame({
        'c': range(num_colors),
        'key': 1
    })
    all_comb = pos
    for i in range(num_pegs-1):
        all_comb = all_comb.merge(pos, how='outer', on='key', suffixes=('_x'+str(i), '_y'+str(i)))
    all_comb = all_comb.drop('key', axis=1)
    all_comb.columns = range(num_pegs)
    return np.array(all_comb)

def scoring(guess, true, num_pegs=4):
    """
    :param: guess:
    :param: true:
    return R (number of correct color and peg), W (number of correct color only but incorrect peg)
    """
    R, W = 0, 0

    # hashmap: storing the true value w.r.t. its occurance
    true_hash = {}
    for i in range(num_pegs):
        if true[i] in true_hash:
            true_hash[true[i]] += 1
        else:
            true_hash[true[i]] = 1

    # avoid duplicated guessing
    # e.g. true = [4,3,2,3]; guess = [1,3,0,5]
    # count num red
    guessed = []
    for i in range(num_pegs):
        if guess[i] == true[i]:
            R += 1
            true_hash[true[i]] -= 1
            guessed.append(i)
    # count num white
    for i in range(num_pegs):
        if guess[i] in true_hash and true_hash[guess[i]] > 0 and not i in guessed:
            W += 1
            true_hash[guess[i]] -= 1

    return R, W

def make_score_table(guesses, possible_comb):
    """
    :param: guesses (np.array):
    :param: possible_comb (np.array):
    return a dataframe with
        columns = all possible guesses
        rows = all possible combinations
        values = the corresponding results e.g. (3, 0) = 3 red and 1 white
    """
    score_table = {}
    for i, guess in tqdm(enumerate(guesses)):
        res = []
        for true in possible_comb:
            res.append(scoring(guess, true))
        score_table[i] = res
    score_table = pd.DataFrame(score_table)
    return score_table
