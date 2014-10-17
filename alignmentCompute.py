#!/usr/bin/env python
'''
this program have four functions, will implement compute a common class
of scoring matrix compute the alignment matrix respectively.
'''

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Takes as input a set of characters alphabet and three scores diag_score,
    off_diag_score, and dash_score.
    Return a dictionary of dictionaries whose entries are indexed by pairs
    of characters in alphabet plus -.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    The score for the remaining off-diagonal entries is  off_diag_score
    '''
    alphabet_temp = set(alphabet)
    alphabet_temp.add('-')
    scoring_matrix = {}
    for row in alphabet_temp:
        scoring_matrix[row] = {}
        for col in alphabet_temp:
            if row == '-' or col == '-':
                scoring_matrix[row][col] = dash_score
            elif row == col:
                scoring_matrix[row][col] = diag_score
            else:
                scoring_matrix[row][col] = off_diag_score
    
    return scoring_matrix
    
def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    if global_flag is True, matrix is computed using the global pairwise alignment
    if global_flag is False, matrix is computed using the local pairwise alignment
    seq_x, seq_y is two sequence to compute alignment
    scoring matrix is the solution of build_scoring_matrix function
    '''
    length_x = len(seq_x)
    length_y = len(seq_y)
    alignment_matrix = [[0 for dummy_col in range(length_y + 1)] for dummy_row in range(length_x + 1)]
    
    for idx in range(1, length_x+1):
        alignment_matrix[idx][0] = alignment_matrix[idx-1][0] + scoring_matrix[seq_x[idx-1]]['-']
        if not global_flag:
            alignment_matrix[idx][0] = max(0, alignment_matrix[idx][0])
    for idx in range(1, length_y+1):
        alignment_matrix[0][idx] = alignment_matrix[0][idx-1] + scoring_matrix['-'][seq_y[idx-1]]
        if not global_flag:
            alignment_matrix[0][idx] = max(0, alignment_matrix[0][idx])
    for idx_x in range(1, length_x+1):
        for idx_y in range(1, length_y+1):
            alignment_matrix[idx_x][idx_y] = max(
                alignment_matrix[idx_x-1][idx_y-1] + scoring_matrix[seq_x[idx_x-1]][seq_y[idx_y-1]],
                alignment_matrix[idx_x-1][idx_y] + scoring_matrix[seq_x[idx_x-1]]['-'],
                alignment_matrix[idx_x][idx_y-1] + scoring_matrix['-'][seq_y[idx_y-1]],
            )
            if not global_flag:
                alignment_matrix[idx_x][idx_y] = max(0, alignment_matrix[idx_x][idx_y])
                
    return alignment_matrix
    
def test_matrixs():
    '''
    test two functions: build_scoring_matrix, compute_alignment_matrix
    '''
    scoring_matrix = build_scoring_matrix(alphabet={'A', 'C', 'T', 'G'}, diag_score=10, off_diag_score=4, dash_score=-6)
    print "test build scoring matrix: ", scoring_matrix
    alignment_matrix = compute_alignment_matrix(seq_x='AA', seq_y='TAAT', scoring_matrix=scoring_matrix, global_flag=True)
    print "test compute alignment matrix: ", alignment_matrix
    alignment_matrix = compute_alignment_matrix(seq_x='AA', seq_y='TAAT', scoring_matrix=scoring_matrix, global_flag=False)
    print "test compute alignment matrix(local alignment): ", alignment_matrix
    
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequence seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix.
    This function compute a global alignment of seq_x and seq_y using the global
    alignment matrix alignment_matrix.
    Return a tuple form (score, align_x, align_y) where score is the score of 
    the global alignment align_x and align_y.
    Align_x and align_y have same length.(add "-")
    '''
    score_optimal = max([max(item) for item in alignment_matrix])
    for item in alignment_matrix:
        if score_optimal in item:
            idx_y = item.index(score_optimal)
            idx_x = alignment_matrix.index(item)
    
    #initial the align_x and align_y, reserve it 
    align_x = seq_x[idx_x:]
    align_y = seq_y[idx_y:]
    align_x = align_x[::-1]
    align_y = align_y[::-1]
    while idx_x and idx_y:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y-1] + scoring_matrix[seq_x[idx_x-1]][seq_y[idx_y-1]]:
            align_x += seq_x[idx_x-1]
            align_y += seq_y[idx_y-1]
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y] + scoring_matrix[seq_x[idx_x-1]]['-']:
                align_x += seq_x[idx_x-1]
                align_y += '-'
                idx_x -= 1
                #import pdb; pdb.set_trace()
            else:
                align_x += '-'
                align_y += seq_y[idx_y-1]
                idx_y -= 1
    while idx_x:
        align_x += seq_x[idx_x-1]
        align_y += '-'
        idx_x -= 1
    while idx_y:
        align_x += '-'
        align_y += seq_y[idx_y-1]
        idx_y -= 1
        
    #reserve the string
    align_x = align_x[::-1]
    align_y = align_y[::-1]
        
    # align_x and align_y have same length
    length_x = len(align_x)
    length_y = len(align_y)
    if length_x < length_y:
        align_x += '-' * (length_y - length_x)
    else:
        align_y += '-' * (length_x - length_y)
        
    #The score need to recalculate, cause there may be '-' more
    score_updated = sum([scoring_matrix[align_x[idx]][align_y[idx]] for idx in range(len(align_x))])

    return score_updated, align_x, align_y
    
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequences seq_x and seq_y whose element share a common
    alphabet with the scoring matrix scoring_matrix.
    This function computes a local alignment of seq_x and seq_y using the local
    matrix alignment_matrix
    Return a tuple of the form (score, align_x, align_y) where the score is the \
    score of the optimal local alignment align_x and align_y
    '''
    score_optimal = max([max(item) for item in alignment_matrix])
    for item in alignment_matrix:
        if score_optimal in item:
            idx_y = item.index(score_optimal)
            idx_x = alignment_matrix.index(item)
    
    align_x = ''
    align_y = ''
    #import pdb; pdb.set_trace()
    while idx_x and idx_y:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y-1] + scoring_matrix[seq_x[idx_x-1]][seq_y[idx_y-1]]:
            align_x += seq_x[idx_x-1]
            align_y += seq_y[idx_y-1]
            #import pdb; pdb.set_trace()
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y] + scoring_matrix[seq_x[idx_x-1]]['-']:
                align_x += seq_x[idx_x-1]
                align_y += '-'
                idx_x -= 1
                #import pdb; pdb.set_trace()
            else:
                align_x += '-'
                align_y += seq_y[idx_y-1]
                idx_y -= 1
            
    #there are '-' on the tail
    while True:
        try:
            if align_x[-1] == '-' or align_y[-1] == '-':
                align_x = align_x[:-1]
                align_y = align_y[:-1]
            else:
                break
        except(IndexError):
            break
                
    #The score need to recalculate, cause the length is less.
        score_updated = sum([scoring_matrix[align_x[idx]][align_y[idx]] for idx in range(len(align_x))])
    
    return score_updated, align_x[::-1], align_y[::-1]
    
    
def test_alignment():
    '''
    test alignment, global and local
    '''
    seq_x='happypedestrianwalker'
    seq_y='sadpedesxtriandriver'
    alphabet = set(seq_x)
    alphabet.update(set(seq_y))
    scoring_matrix = build_scoring_matrix(alphabet=alphabet, diag_score=2, off_diag_score=-1, dash_score=-1)
    alignment_matrix = compute_alignment_matrix(seq_x=seq_x, seq_y=seq_y, scoring_matrix=scoring_matrix, global_flag=True)
    alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    print "test global alignment: ", alignment, alignment_matrix
    
    #test local alignment
    alignment_matrix = compute_alignment_matrix(seq_x=seq_x, seq_y=seq_y, scoring_matrix=scoring_matrix, global_flag=False)
    alignment = compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    print "test local alignment: ", alignment, alignment_matrix

if __name__ == "__main__":
    #test_matrixs()
    test_alignment()