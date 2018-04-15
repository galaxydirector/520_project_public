#!/usr/bin/python

import nltk
import os
nltk.data.path.append(os.getcwd() + '/dataset/')
from nltk.corpus import semcor

from nltk.stem.wordnet import WordNetLemmatizer
import re
import pickle
import numpy as np

def load_tag_fies(index_file):
    tag_files = []
    with open(index_file) as f:
        for line in f:
            tag_files.append(line.replace('\n',''))
    return tag_files

def load(filename):
    if os.path.isfile(filename):
        print 'Load from %s' % filename
        with open(filename) as f:
            [data,] = pickle.load(f)
        return data
    else: return None

def save(data, filename):
    print 'Saving to %s' % filename
    with open(filename, 'w') as f:
        pickle.dump([data,], f)

class WordParser:
    def __init__(self):
        self.pattern = re.compile('[a-z]+')

    def filter(self,line):
        return ('WORD: ' in line)

    def map(self,word):
        return self.pattern.findall(word)[0]

class WordFilter:
    def __init__(self, min_sense_appre=10):
        self.min_sense_appre = min_sense_appre
    def filter(self, stat):
        return (len(stat.values()) >= self.min_sense_appre)

class WordStat:
    def __init__(self, init_map={}):
        self.senses = init_map
    def update(self, x):
        if x == None: return
        if not x.isdigit(): return

        if x not in self.senses.keys():
            self.senses[x] = 0
        self.senses[x] += 1
    def dump(self):
        for k,v in self.senses.items():
            print k,v
    def keys(self):
        return self.senses.keys()
    def items(self):
        return self.senses.items()

class SemcorParser:
    def __init__(self, index_file, force_update=False):
        # try to load from pickle file first
        pkl_file = 'pickle/word_map.pkl'
        loaded = load(pkl_file)

        if loaded != None and force_update==False:
            self.word_map = loaded
        else:
            self.word_map = {}
            # have to parse corpose
            tag_files = load_tag_fies(index_file)
            for f in tag_files:
                self.parse(f)
            save(self.word_map, pkl_file)

    def parse(self,filename):
        # get sentence from semcor file
        print 'parsing %s...' % filename
        sentences = semcor.xml(filename).findall('context/p/s')

        for sent in sentences:
            for wordform in sent.getchildren():
                lemma = wordform.get('lemma')
                sense_id = wordform.get('wnsn')

                if lemma not in self.word_map.keys():
                    self.word_map[lemma] = WordStat()
                self.word_map[lemma].update(sense_id)

class WordContext:
    class Context:
        def __init__(self,sent,sense_id):
            self.sent = sent
            self.sense_id = sense_id
        def __str__(self):
            _str = ''
            for wf in self.sent.getchildren():
                _str += '%s ' % wf.text
            return _str

    def __init__(self):
        self.stats = []
    def update(self, sent, sense_id):
        self.stats.append(Context(sent, sense_id))
    def dump(self):
        for i,c in enumerate(self.stats):
            print 'context%d: %s' % (i,str(c))

def filter_word_map(word_map, min_sense_appr):
    filtered_map = {}
    for word, senses in word_map.items():
        dense_senses = {}
        for sid, count in senses.items():
            if count > min_sense_appr:
                dense_senses[sid] = count
        if len(dense_senses.keys()) > 1: 
            filtered_map[word] = WordStat(dense_senses)
        else:
            print sid, count
    return filtered_map

if __name__ == '__main__':
    tag_file = './dataset/semcor_tagfiles_full.txt'
    word_map = SemcorParser(tag_file,force_update=False).word_map

    MIN_SENSE_APPR = 1000
    ambiguous_words = filter_word_map(word_map, MIN_SENSE_APPR)
    print '%d ambiguous words' % len(ambiguous_words.keys())
