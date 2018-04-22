#!/usr/bin/python

import os
import numpy as np
from collections import defaultdict
from sklearn.model_selection import train_test_split

out_dir = './dataset/word_pos'
sub_dirs = ['X_train', 'Y_train', 'X_test', 'Y_test']
for d in sub_dirs:
    _dir = '%s/%s' %(out_dir,d)
    if not os.path.exists(_dir):
        os.makedirs(_dir)

with open('./word_list.txt') as f:
# with open('./small.txt') as f:
    for w in f:
        w = w.rstrip()
        dataset = './dataset/words/%s' % w

        matrix = np.loadtxt(dataset,delimiter=',')
        X = matrix[:,:-1]
        y = matrix[:,-1]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                test_size=0.2, stratify=y, random_state=42)
    
        np.savetxt('%s/X_train/%s' %(out_dir,w), X_train,delimiter=',')
        np.savetxt('%s/Y_train/%s' %(out_dir, w), y_train,delimiter=',')
        np.savetxt('%s/X_test/%s' %(out_dir, w), X_test,delimiter=',')
        np.savetxt('%s/Y_test/%s' %(out_dir, w), y_test,delimiter=',')
