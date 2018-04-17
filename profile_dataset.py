#!/usr/bin/python

import numpy as np
from collections import defaultdict

with open('./word_list.txt') as f:
    for word in f:
        dataset = './dataset/words/%s' % word.rstrip()

        matrix = np.loadtxt(dataset,delimiter=',')
        print '\n%ssize:%s' %(word, str(matrix.shape))
        labels = matrix[:,-1]

        freq = defaultdict(int)
        for l in labels:
            freq[l] += 1
        print 'sense id, frequncy'
        for sid, count in freq.items():
            print '%d: %d' %(sid, count)
