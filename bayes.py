#!/usr/bin/python

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import numpy as np

def train_bayes (X,y):
    gnb = GaussianNB()
    y_pred = gnb.fit(X, y)
    return gnb

def load_data (filename):
    matrix = np.loadtxt(filename,delimiter=',')
    return matrix

def dump_score(filename, words, scores):
    with open(filename, 'w') as f:
        for w,s in zip(words,scores):
            f.write('%s: %.4f\n' % (w,s))

if __name__ == '__main__':
    # data_dir = './dataset/word_pos'
    # vocab = 'word_list.txt'
    # length = 8
    data_dir = './dataset/word_pos_large'
    vocab = 'large.txt'
    length = 2

    accuracies = np.zeros(length)
    f1scores = np.zeros(length)

    i = 0
    words = []
    with open(vocab) as f:
        for w in f:
            w = w.rstrip()
            print 'training on ', w
            words.append(w)
            X_train_file = '%s/X_train/%s' % (data_dir,w)
            Y_train_file = '%s/Y_train/%s' % (data_dir,w)
            X = load_data(X_train_file)
            y = load_data(Y_train_file)

            classifier = train_bayes(X,y)
            
            X_test_file = '%s/X_test/%s' % (data_dir,w)
            Y_test_file = '%s/Y_test/%s' % (data_dir,w)
            X_test = load_data(X_train_file)
            y_test = load_data(Y_train_file)

            y_pred = classifier.predict(X_test)
            accuracies[i] = metrics.accuracy_score(y_test,y_pred)
            f1scores[i] = metrics.f1_score(y_test,y_pred,average='weighted')

            i += 1

    dump_score('bayes_f1.log', words, f1scores)
    dump_score('bayes_accuracy.log', words, f1scores)
    np.savetxt('bayes_f1.txt', accuracies, delimiter=',')
    np.savetxt('bayes_accuracy.txt', accuracies, delimiter=',')
