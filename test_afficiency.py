#! /usr/bin/env python
'''
test some module's efficiency
'''
import random
import timeit

STRING_SAMPLE = 'MQNSHSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQMGADGMYDKLRMLNGQTGSWGTRPGWYPGTSVPGQPTQDGCQQQEGGGENTNSISSNGEDSDEAQMRLQLKRKLQRNRTSFTQEQIEALEKEFERTHYPDVFARERLAAKIDLPEARIQVWFSNRRAKWRREEKLRNQRRQASNTPSHIPISSSFSTSVYQPIPQPTTPVSSFTSGSMLGRTDTALTNTYSALPPMPSFTMANNLPMQPPVPSQTSSYSCMLPTSPSVNGRSYDTYTPPHMQTHMNSQPMGTSGTTSTGLISPGVSVPVQVPGSEPDMSQYWPRLQ'
LIST_SAMPLE = random.sample(range(1000), 100)

def string_shuffle_list():
    '''
    shuffle the string with list
    '''
    string_list = list(STRING_SAMPLE)
    random.shuffle(string_list)
    string_shuffle = ''.join(string_list)
    return
    
def string_shuffle_sample():
    '''
    shuffle the string with sample
    '''
    string_shuffle = ''.join(random.sample(STRING_SAMPLE, len(STRING_SAMPLE)))
    return
    
def test_shuffle_efficiency():
    t2 = timeit.Timer("string_shuffle_sample()", "from __main__ import string_shuffle_sample")
    t1 = timeit.Timer("string_shuffle_list()", "from __main__ import string_shuffle_list")
    print("string shuffle with list: %s,\nstring shuffle with sample: %s" %(t1.timeit(), t2.timeit()))

def max_iteration(list_sample):
    length = len(list_sample)
    if length <= 1:
        return list_sample[0]
    max1 = max_iteration(list_sample[:length/2])
    max2 = max_iteration(list_sample[length/2:])
    return max(max1, max2)
    
def max_original(list_sample):
    return max(list_sample)
    
def test_max():
    t1 = timeit.Timer(lambda: max_iteration(LIST_SAMPLE))
    t2 = timeit.Timer(lambda: max_original(LIST_SAMPLE))
    print("max iteration: %s \nmax original: %s" %(t1.timeit(), t2.timeit()))
    
def sort_iteration(list_sample):
    #merges sort
    
    result = []
    length = len(list_sample)
    if length <= 1:
        return list_sample
    list1 = sort_iteration(list_sample[:length/2])
    list2 = sort_iteration(list_sample[length/2:])
    while (len(list1) > 0) or (len(list2) > 0):
        if (len(list1) > 0) and (len(list2) > 0):
            if list1[0] < list2[0]:
                result.append(list1.pop(0))
            else:
                result.append(list2.pop(0))
        elif len(list1) == 0:
            result.extend(list2)
            list2 = []
        elif len(list2) == 0:
            result.extend(list1)
            list1 = []
        else:
            print "something is wrong."
            raise
    return result
    
def sort_original(list_sample):
    return sorted(list_sample)
    
def test_sort():
    t1 = timeit.Timer(lambda: sort_iteration(LIST_SAMPLE))
    t2 = timeit.Timer(lambda: sort_original(LIST_SAMPLE))
    print("sort iteration: %s \nsort original: %s" %(t1.timeit(), t2.timeit()))
        
if __name__ == '__main__':
    #test_shuffle_efficiency()
    test_max()
    #test_sort()
