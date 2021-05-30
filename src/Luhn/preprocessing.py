import csv
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import numpy as np
import re
from collections import defaultdict, Counter


class Converter(Tokenizer):
    def __init__(self, f, keyword):
        self.f = f
        self.keyword = keyword

    def getAnswer(self, QAlist):
        question = QAlist[0]
        ans = QAlist[1]
        if self.keyword in question:
            return ans
        return ""

    def normalize(self, document):
        document = document.lower()
        sentences = re.findall(".*?。", re.sub('<br/>|<p>|</p>','',document))
        return sentences

    def getDocuments(self):
        docs = []
        for QAlist in self.f:
            ans = self.getAnswer(QAlist)
            if ans != "":
                doc = self.normalize(ans)
                docs.append(doc)
        return docs
    
    def flatten(self, docs):
        docLong = []
        for doc in docs:
            docLong.extend(doc)
        return docLong
    
    def freqDict(self, sentences):
        tokenizer = Tokenizer()
        all_tokens = []
        for sentence in sentences:
            tokens = tokenizer.tokenize(sentence)
            for token in tokens:
                all_tokens.append(token.base_form)
        FreqDict = Counter(all_tokens)
        return FreqDict
    
    def freqNoun(self, sentences, N=-1):
        tokenizer = Tokenizer()
        all_tokens = []
        allSentences  = ''.join(sentences)
        
        #tokens = tokenizer.tokenize(sentences)
        #for token in tokens:
        #    print(token)
        a = Analyzer(token_filters=[POSKeepFilter(['名詞']), TokenCountFilter(sorted=True)])
        g_count = list(a.analyze(allSentences))[:N]
        return g_count


if __name__=="__main__":
    with open('../../data/gs.csv','r') as csvfile:
        f = csv.reader(csvfile)
        converter = Converter(f, "長所")
        docs = converter.getDocuments()
        sentences = converter.flatten(docs)
        
        importantWords = converter.freqNoun(sentences, 100)
        for c in importantWords:
            print(c)

        #word_idx = []

        # 単語リスト中の個々の単語について
        #for w, _ in importantWords:
            #try:
            #    # 文中の重要単語が出現した位置のインデックスを計算する
            #    word_idx.append(sentences.index(w))
            #except ValueError, sentences:  # この文にはwが含まれていない
            #    pass

        #word_idx.sort()

        # 一部の文は、重要単語を１つも含んでいないことがありえる
        #if len(word_idx) == 0:
        #    continue