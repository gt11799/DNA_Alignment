#! /usr/bin/env python
'''
Given the HumanEyelessprotein and FruitflyEyelessrotein, compute the local
alignment of the two protein, get the score(similarity).
'''

import difflib
import random
from alignmentCompute import compute_alignment_matrix, compute_local_alignment, compute_global_alignment

def read_protein(filename):
    '''
    Read a protein sequence from the file named filename
    
    Arguments:
    filename -- name of file containing a protein sequence
    
    Returns:
    A string representing the protein
    '''
    protein_file = open(filename, 'r')
    protein_seq = protein_file.read()
    protein_file.close()
    protein_Seq = protein_seq.rstrip()   #maybe a space on the tail
    
    return protein_seq
    
def read_scoring_matrix(filename):
    '''
    Read a scoring matrix from the file named filename.
    
    Argument:
    filename -- name of file containing a scoring matrix
    
    Returns:
    A dictionary of dictionaries mapping X and Y characters to score.
    '''
    scoring_dict = {}
    scoring_file = open(filename, 'r')
    ykeys = scoring_file.readline()   #iteration, call will carry on
    ykeychars = ykeys.split()
    
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict
    
def test_read_file():
    protein = read_protein('FruitflyEyelessProtein.txt')
    scoring_matrix = read_scoring_matrix('score_PAM50.txt')
    print("protein: %r \nscoring_matrix: %s" %(protein, scoring_matrix))
    
def protein_alignment(scoring_matrix):
    '''
    compute the human eyeless protein and fruitfly eyeless portein alignment
    '''
    human_protein = read_protein('HumanEyelessProtein.txt')
    fruitfly_protein = read_protein('FruitflyEyelessprotein.txt')
    
    alignment_matrix = compute_alignment_matrix(seq_x=human_protein, seq_y=fruitfly_protein, scoring_matrix=scoring_matrix, global_flag=False)
    score, align_human, align_fruitfly = compute_local_alignment(seq_x=human_protein, seq_y=fruitfly_protein, scoring_matrix=scoring_matrix, alignment_matrix=alignment_matrix)
    return score, align_human, align_fruitfly
    
def consensus_alignment(scoring_matrix, align_sequence):
    '''
    compute the similarity of the two sequences in the local alignment computed to
    the PAX Domain.
    global alignment of local align_x vs PAX Domain, local align_y vs PAX Domain
    return the alignment and the persentage of elements in these two sequences that agree
    '''
    pax_domain = read_protein('ConsensusPAXDomain.txt')

    align_sequence = align_sequence.replace("-", "")
    alignment_matrix = compute_alignment_matrix(seq_x=align_sequence, seq_y=pax_domain, scoring_matrix=scoring_matrix, global_flag=True)
    score, global_align_sequence, global_align_pax = compute_global_alignment(seq_x=align_sequence, seq_y=pax_domain, scoring_matrix=scoring_matrix, alignment_matrix=alignment_matrix)
    seq = difflib.SequenceMatcher(None, global_align_sequence, global_align_pax)
    ratio = seq.ratio()
    #import pdb; pdb.set_trace()

    
    return global_align_sequence, ratio
    
def random_alignment(scoring_matrix):
    '''
    Take two random amino acids, compute the alignment and the consensus with pax
    Return the ratio of similarity
    To examine the solution of the homework
    '''
    alphabet = "ACBEDGFIHKMLNQPSRTWVYXZ"
    length_human = 422
    length_fruitfly = 857
    
    random_human = ''
    for _ in range(length_human):
        random_human += random.choice(alphabet)
    
    random_fruitfly = ''
    for _ in range(length_fruitfly):
        random_fruitfly += random.choice(alphabet)
        
    alignment_matrix = compute_alignment_matrix(seq_x=random_human, seq_y=random_fruitfly, scoring_matrix=scoring_matrix, global_flag=False)
    score, align_human, align_fruitfly = compute_local_alignment(seq_x=random_human, seq_y=random_fruitfly, scoring_matrix=scoring_matrix, alignment_matrix=alignment_matrix)
    
    global_align_human, ratio_human_random = consensus_alignment(scoring_matrix, align_human)
    global_align_fruitfly, ratio_fruitfly_random = consensus_alignment(scoring_matrix, align_fruitfly)
    
    return ratio_human_random, ratio_fruitfly_random
    
if __name__ == '__main__':
    
    scoring_matrix = read_scoring_matrix('score_PAM50.txt')    
    
    score, align_human, align_fruitfly = protein_alignment(scoring_matrix)
    #print("The alignment of human eyeless protein and fruitfly eyeless protein is as :\n score: %s\n Human alignment: %s\n Fruitfly alignment: %s" %(score, align_human, align_fruitfly))
    
    global_align_human, human_ratio = consensus_alignment(scoring_matrix, align_human)
    global_align_fruitfly, fruitfly_ratio = consensus_alignment(scoring_matrix, align_fruitfly)
    
    print("The consensus alignment is as: \n human to PAX Domain: %s\n fruitfly to PAX Domain: %s\n similarity of human aligned and PAX aligned: %s\n similarity of fruitfly aligned and PAX aligned %s"\
        %(global_align_human, global_align_fruitfly, human_ratio, fruitfly_ratio ))
        
    ratio_human_random, ratio_fruitfly_random = random_alignment(scoring_matrix)
    print("Similarity of random sequences of length of human is: %s, fruitfly is: %s" %(ratio_human_random, ratio_fruitfly_random))
    