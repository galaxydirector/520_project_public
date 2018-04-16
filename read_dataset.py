#!/usr/bin/python

import numpy as np

dataset = './dataset/words/person.txt'

matrix = np.loadtxt(dataset,delimiter=',')
print matrix.shape
print matrix[19,:]
