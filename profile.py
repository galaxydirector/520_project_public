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

    num_new_words = 0
    num_words = 0

    for sent in sentences:
        for wordform in sent.getchildren():
            num_words += 1

            lemma = wordform.get('lemma')
            sense_id = wordform.get('wnsn')

            if lemma in word_map.keys():
                stat = word_map[lemma]
                if sense_id in stat.keys():
                    stat[sense_id] += 1
                else:
                    stat[sense_id] = 1
            else:
                num_new_words += 1

                stat = {}
                stat[sense_id] = 1
                word_map[lemma] = stat

    # stats
    print ('sentences: %d' % len(sentences))
    print ('words: %d' % num_words)
    print ('%.0f words / sentence' % (num_words / len(sentences)))
    print ('new words: %d' % num_new_words)

    return word_map

def find_ambiguous_words(word_map):
    sense_number_map = np.zeros(100)
    ambiguous_words = {}
    for word, sense_map in word_map.items():
        num_sense = len(sense_map.keys())
        sense_number_map[num_sense] += 1

        if num_sense > 1:
            ambiguous_words[word] = sense_map

    return ambiguous_words

def load_tag_fies(index_file):
    tag_files = []
    with open(index_file) as f:
        for line in f:
            tag_files.append(line.replace('\n',''))

    return tag_files

if __name__ == '__main__':
    tag_files = load_tag_fies('./dataset/semcor_tagfiles_full.txt')
    # tag_files = load_tag_fies('./dataset/brown1_tagfiles.txt')
    filename = 'brown2/tagfiles/br-n12.xml'
    word_map = {}
    for t in tag_files:
        print ('parsing %s ...' % t)
        word_map = profile_file(word_map,t)
        print ('total words: %d' % len(word_map.keys()))

    ambiguous_words = find_ambiguous_words(word_map)
    for word, sense_map in ambiguous_words.items():
        print (word)
        for sense_id, count in sense_map.items():
            print ('sense %s appears %d times' %(sense_id, count))
        print ('')

    print ('number of ambiguous words: %d' % len(ambiguous_words.keys()))
