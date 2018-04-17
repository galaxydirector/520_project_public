# from nltk.stem.wordnet import WordNetLemmatizer
import collections
from nltk.corpus import semcor
import numpy as np

from misc import *

class Context:
    ''' x_i: vector
        y_i: sense_id
        word_list: list of word as string, for debugging
    '''
    def __init__(self, vector, sense_id, word_list):
        self.vector = vector
        self.sense_id = int(sense_id)
        self.word_list = word_list
    def dump(self):
        print 'words: %s\n vector: %s, sense id: %d' % (str(self.word_list) ,self.vector, self.sense_id)
    def vec(self):
        return np.append(self.vector, [self.sense_id])

class ContextContainer:
    def __init__(self, text):
        self.text = text
        self.context_list = np.array([])
    def update(self, vector, sense_id, word_list):
        self.context_list = np.append(self.context_list,Context(vector,
            sense_id, word_list))

    def dump(self,n=1):
        # sample some instance and print to screen
        for i,c in enumerate(self.context_list):
            if i > n: break
            c.dump()

    def len(self):
        return len(self.context_list)

    def dump2file(self, filename):
        vector_list = map(lambda x: x.vec(), self.context_list)
        matrix = reduce(lambda x,y: np.vstack((x,y)), vector_list)
        np.savetxt(filename,matrix,delimiter=',')

class ContextExtractor:
    def __init__(self, word_map, word2vec_model):
        self.word_map = word_map
        self.contexts = {}
        self.word2vec_model = word2vec_model
        self.WORD_VECTOR_LEN = 100

    def go(self, index_file):
        tag_files = load_tag_fies(index_file)
        for t in tag_files:
            print 'scannig %s' % t
            self.__scan_corpus(t)

    def __scan_corpus(self, filename):
        # get sentence from semcor file
        sentences = semcor.xml(filename).findall('context/p/s')

        for sent in sentences:
            for wordform in sent.getchildren():
                lemma = wordform.get('lemma')
                sense_id = wordform.get('wnsn')
                text = wordform.text

                # check that both word and sense id are in word_map
                if lemma in self.word_map.keys():
                    if sense_id in self.word_map[lemma].keys():
                        self.__parse(text,lemma, sent, sense_id)

    def __parse(self, word, lemma, sent, sense_id):
        # from word to a matrix representation
        if lemma not in self.contexts.keys():
            self.contexts[lemma] = ContextContainer(word)
        vector,word_list = self.__sent2vec(word, sent)
        self.contexts[lemma].update(vector, sense_id, word_list)

    @staticmethod
    def __combine_bufs(last_words,next_words):
        return reduce(lambda x,y: np.append(x,y), np.append(last_words,
            next_words))

    def __word2vec(self, word, pos_tag):
        # TODO: incooperate POS tag informatoin
        return self.word2vec_model[word]

    def __sent2vec(self, word, sent):
        WINDOW_SIZE = 2
        last_words = collections.deque(maxlen=WINDOW_SIZE)
        next_words = collections.deque(maxlen=WINDOW_SIZE)
        padding = np.zeros(self.WORD_VECTOR_LEN)
        word_list = []
        for i in range(WINDOW_SIZE):
            last_words.append(padding)
            next_words.append(padding)
        is_seen = False
        look_ahead = 0
        for wf in sent.getchildren():
            pos_tag = wf.get('POS')
            lemma = wf.get('lemma')
            word_list.append(wf.text)

            if wf.text == word:
                is_seen = True

            if word in self.word2vec_model.wv.vocab:
                _vec = self.__word2vec(word,pos_tag)
                if is_seen and look_ahead < WINDOW_SIZE:
                    next_words.append(_vec)
                    look_ahead += 1
                else:
                    last_words.append(_vec)
        assert is_seen == True
        return self.__combine_bufs(last_words,next_words), word_list

    def dump(self):
        for i,w in enumerate(self.contexts.keys()):
            if i>3: break
            print w
            self.contexts[w].dump()

    def dump2file(self):
        for w,c in self.contexts.items():
            if c.len() > 100:
                filename = './dataset/words/%s.txt' % w
                print 'dumpping %s to %s' % (w,filename)
                c.dump2file(filename)