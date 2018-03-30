#!/usr/bin/python

# Haoxian: This script is for profiling the stats of the corpus

from __future__ import print_function
import nltk
import os
nltk.data.path.append(os.getcwd() + '/dataset/')
from nltk.corpus import semcor
import numpy as np

def profile_file(word_map, filename):
    # get sentence from semcor file
    sentences = semcor.xml(filename).findall('context/p/s')

    # init_the word_map if empty
    if len(word_map.keys()) == 0:
        word_map = {}

    for sent in sentences:
        for wordform in sent.getchildren():
            lemma = wordform.get('lemma')
            sense_id = wordform.get('wnsn')

            if lemma in word_map.keys():
                stat = word_map[lemma]
                if sense_id in stat.keys():
                    stat[sense_id] += 1
                else:
                    stat[sense_id] = 1
            else:
                stat = {}
                stat[sense_id] = 1
                word_map[lemma] = stat

    # stats
    print ('number of sentences: %d' % len(sentences))
    print ('number of words: %d' % len(word_map.keys()))

    return word_map

def find_ambiguous_words(word_map):
    sense_number_map = np.zeros(20)
    ambiguous_words = {}
    for word, sense_map in word_map.items():
        num_sense = len(sense_map.keys())
        sense_number_map[num_sense] += 1

        if num_sense > 1:
            ambiguous_words[word] = sense_map

    return ambiguous_words

if __name__ == '__main__':
    filename = 'brown2/tagfiles/br-n12.xml'
    word_map = {}
    word_map = profile_file(word_map,filename)

    ambiguous_words = find_ambiguous_words(word_map)
    for word, sense_map in ambiguous_words.items():
        print (word)
        for sense_id, count in sense_map.items():
            print ('sense %s appeaars %d times' %(sense_id, count))
        print ('\n')
