#! /usr/bin/env python
'''
'''

import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from alignmentCompute import compute_alignment_matrix, compute_local_alignment
from eyelessProteinAlign import read_protein, read_scoring_matrix

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    '''
    Takes as input two sequences seq_x and seq_y, a scoring matrix scoring_matrix,
    and a number of trials num_trials.
    Return a dictionary scoring_distribution that represents an un-normalized 
    distribution generated by performing the following process num_trials times:
    1.Generate a random permutation rand_y of the sequence seq_y using random.shuffle()
    2.Compute the maximum value score for the local alignment of seq_x and rand_y
    3.Increment the entry score in the dictionary scoring_distribution by one.
    '''
    scoring_distribution = {}
    for _ in range(num_trials):
        
        #shuffle the seq_y
        list_y = list(seq_y)
        random.shuffle(list_y)
        rand_y = "".join(list_y)
        alignment_matrix = compute_alignment_matrix(seq_x=seq_x, seq_y=rand_y, scoring_matrix=scoring_matrix, global_flag=False)
        score = max([max(item) for item in alignment_matrix])
        #score, align_human, align_fruitfly = compute_local_alignment(seq_x=seq_x, seq_y=rand_y, scoring_matrix=scoring_matrix, alignment_matrix=alignment_matrix)
        #import pdb; pdb.set_trace()
        try:
            scoring_distribution[score] += 1
        except(KeyError):
            scoring_distribution[score] = 1
        
    scoring_file = open('scoring_distribution.p', 'wb')
    pickle.dump(scoring_distribution, scoring_file)
    scoring_file.close()
        
    return scoring_distribution
    
def get_distribution():
    try:
        scoring_file = open('scoring_distribution.p', 'rb')
        scoring_distribution = pickle.load(scoring_file)
        scoring_file.close()
    except:
        human_protein = read_protein('HumanEyelessProtein.txt')
        fruitfly_protein = read_protein('FruitflyEyelessProtein.txt')
        scoring_matrix = read_scoring_matrix('score_PAM50.txt')
        scoring_distribution = generate_null_distribution(seq_x=human_protein, seq_y=fruitfly_protein, scoring_matrix=scoring_matrix, num_trials=1000)
    return scoring_distribution
    
def plot_null_distribution():
    '''
    Plot the scoring_distribution from generate_null_distribution, 
    The horizontal axis is the scores and the vertical axis is the 
    fraction of total trials corresponding to each score.
    '''
    scoring_distribution = get_distribution()
    
    axis_x = scoring_distribution.keys()
    axis_y = scoring_distribution.values()
    sum_y = float(sum(axis_y))
    axis_y = np.array(axis_y) / sum_y
    
    plt.title('Statistical hypothesis test')
    plt.xlabel('Score of local alignment')
    plt.ylabel('Normalization of frequency')
    plt.bar(axis_x, axis_y, width=1.0, bottom=None)
    plt.show()
    
def statistical_analysis():
    '''
    compute the mean, standard deviation of the distribution, and a-score of the
    local alignment of HumanEyelessProtein and FruitflyEyelessProtein.
    z-score = (s - mean) / standard_deviation
    The z-score help quantify the likelihood of the score s being a product of chance.
    return  mean, standard deviation, z-score 
    '''
    score_human_fruitfly = 757.0
    scoring_distribution = get_distribution()
    score = scoring_distribution.keys()
    length = len(score)
    
    mean = sum(score) / float(length)
    diff_square = np.square(np.array(score) - mean)
    standard_deviation = np.sqrt(sum(diff_square) / float(length))
    z_score = (score_human_fruitfly - mean) / standard_deviation
    
    return mean, standard_deviation, z_score
    
if __name__ == "__main__":
    #plot_null_distribution()
    mean, standard_deviation, z_score = statistical_analysis()
    print("statistical analysis \nmean: %s\nstandard deviation: %s\nz_score: %s"\
        %(mean, standard_deviation, z_score))
        
    #compare with the lottery jackpot record
    import math
    f_human_fruitfly = 1 - math.erf(z_score / math.sqrt(2))
    f_lottery = (1 / 100000.0) ** 18
    print("frequency of human vs fruitfly: %s\nfrequency of extremely large lottery: %s"\
        %(f_human_fruitfly, f_lottery))