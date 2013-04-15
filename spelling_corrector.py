#!/usr/bin/env python

import string
import os
import sys

DICTIONARY = {}

def read_words():
    '''
    Read bag of words from file
    '''
    f = open('wiktionary', 'r')
    for line in f.readlines():
        DICTIONARY.update({line.split(':')[0] : float(line.split(':')[1])})

def generate_edit_distance1_words(word):
    '''
    Generate a set of all words that are one edit distance from word
    '''
    #delete a character for word
    deletes = [word[1:]]
    deletes += [str(word[:i] + word[i+1:]) for i in range(1, len(word))]
    #change position between two character for word
    transposes = [str(word[1] + word[0] + word[2:])]
    transposes += [str(word[:i-1] + word[i] + word[i-1] + word[i+1:]) for i in range(2, len(word))]
    #replaces one character
    replaces = [str(c + word[1:]) for c in string.lowercase]
    replaces += [str(word[:i] + c + word[i+1:]) for i in range(1, len(word)) for c in string.lowercase]
    #insert one character
    inserts = [str(c + word) for c in string.lowercase]
    inserts += [str(word[:i] + c + word[i:]) for i in range(1, len(word)) for c in string.lowercase]
    inserts += [str(word + c) for c in string.lowercase]

    return set(deletes + transposes + replaces +inserts)

def words_filter(words):
    '''
    Word filter
    '''    
    return set(word for word in words if word in DICTIONARY.keys())

def candidates(word):
    '''
    Get all candidates for word
    '''
    if word in DICTIONARY.keys():
        return set([word])
    else:
        return words_filter([word]) | words_filter(generate_edit_distance1_words(word)) 

def correct(word):
    '''
    correct the word.
    '''
    candidate_words = candidates(word)
    candidate_dict = {}
    for item in candidate_words:
        candidate_dict.setdefault(item, 0)
        candidate_dict.update({item : DICTIONARY[item]})
    
    return max(candidate_dict, key = lambda x : candidate_dict[x])

if __name__ == '__main__':
    read_words()
    print sys.argv[1], '->', correct(sys.argv[1])
