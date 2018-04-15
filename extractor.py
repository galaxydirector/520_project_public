# from nltk.stem.wordnet import WordNetLemmatizer
import collections
from nltk.corpus import semcor

def load_tag_fies(index_file):
    tag_files = []
    with open(index_file) as f:
        for line in f:
            tag_files.append(line.replace('\n',''))
    return tag_files

class Context:
    def __init__(self, vector, sense_id):
        self.vector = vector
        self.sense_id = sense_id
    def dump(self):
        print 'vector: %s, sense id: %s' % (self.vector, self.sense_id)

class ContextContainer:
    def __init__(self, text):
        self.text = text
        self.context_list = []
    def update(self, vector, sense_id):
        self.context_list.append(Context(vector, sense_id))

    def dump(self):
        for c in self.context_list:
            c.dump()

class ContextExtractor:
    class Word:
        def __init__(self,word,pos_tag):
            self._vector = [0]

        @property
        def vector(self):
            return self._vector

    def __init__(self, word_map):
        self.word_map = word_map
        self.contexts = {}

    def go(self, index_file):
        tag_files = load_tag_fies(index_file)
        for t in tag_files:
            self.__scan_corpus(t)

    def __scan_corpus(self, filename):
        # get sentence from semcor file
        sentences = semcor.xml(filename).findall('context/p/s')

        for sent in sentences:
            for wordform in sent.getchildren():
                lemma = wordform.get('lemma')
                sense_id = wordform.get('wnsn')
                text = wordform.text

                if lemma in self.word_map.keys():
                    if sense_id in self.word_map[lemma].keys():
                        self.parse(text,lemma, sent, sense_id)

    def parse(self, word, lemma, sent, sense_id):
        # from word to a matrix representation
        if lemma not in self.contexts.keys():
            self.contexts[lemma] = ContextContainer(word)
        vector = self.__sent2vec(word, sent)
        self.contexts[lemma].update(vector, sense_id)

    @staticmethod
    def __combine_bufs(last_words,next_words):
        return list(last_words) + list(next_words)

    def __sent2vec(self, word, sent):
        WINDOW_SIZE = 2
        last_words = collections.deque(maxlen=WINDOW_SIZE)
        next_words = []
        buf = last_words
        is_seen = False
        for wf in sent.getchildren():
            pos_tag = wf.get('POS')
            if wf.text == word:
                buf = next_words
                is_seen = True
            else:
                buf.append(self.Word(word,pos_tag).vector)
                if is_seen and len(buf) == WINDOW_SIZE:
                    break
        return self.__combine_bufs(last_words,next_words)

    def dump(self):
        for i,w in enumerate(self.contexts.keys()):
            if i>3: break
            print w
            self.contexts[w].dump()
