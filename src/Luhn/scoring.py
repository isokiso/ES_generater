import numpy as np
import re
import csv
from janome.tokenizer import Tokenizer
import sys

from preprocessing import Converter
import parser


class Luhn():
    def __init__(self, importantWords):
        self.importantWords = importantWords
        self.tokenizer = Tokenizer()
        self.CLUSTER_THRESHOLD = 3

    def get_important_index(self, sentence):
        inputTokens = list(self.tokenizer.tokenize(sentence, wakati=True))
        word_idx = []
        for w,_ in self.importantWords:
            try:
                # 文中の重要単語が出現した位置のインデックスを計算する
                word_idx.extend([n for n, v in enumerate(inputTokens) if v == w])
            except ValueError:  # この文にはwが含まれていない
                pass
        word_idx.sort()
        return word_idx
    
    def score_sentence(self, sentence):
        word_idx = self.get_important_index(sentence)
        if len(word_idx) == 0:
            return 0
        clusters = []
        cluster = [word_idx[0]]
        i = 1
        while i < len(word_idx):
            if word_idx[i] - word_idx[i-1] < self.CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1
        clusters.append(cluster)
        
        score_list = []
        max_cluster_score = 0
        
        score_func = lambda cluster: 1.0 * len(cluster)**2 / (cluster[-1] - cluster[0] + 1)
        scores = list(map(score_func, clusters))
        return max(scores)

if __name__=="__main__":
    args = parser.get_option()
    Q = args.question
    LENGTH = int(args.length)

    with open('../../data/gs.csv','r') as csvfile:
        f = csv.reader(csvfile)
        converter = Converter(f, Q)
        docs = converter.getDocuments()
        sentences = converter.flatten(docs)
        sentences = list(set(sentences))
    
        importantWords = converter.freqNoun(sentences, 100)
    
    model = Luhn(importantWords)
    score_list = np.array(list(map(model.score_sentence, sentences)))
    top_sentences = np.argsort(-score_list)
    generated_doc = ""
    for sentence_id in top_sentences:
        if len(generated_doc + sentences[sentence_id]) > LENGTH:
            break
        generated_doc += sentences[sentence_id]
        
    print("keyword of question")
    print(generated_doc)
    print("Word count: ", len(generated_doc))
        
        
        
        
        