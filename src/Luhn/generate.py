import numpy as np
import re
import csv
from janome.tokenizer import Tokenizer
import sys

import parser
from preprocessing import Converter
from scoring import Luhn


if __name__=="__main__":
    args = parser.get_option()
    Q = args.question
    LENGTH = int(args.length)
    print("keyword of question: ", Q)
    print("maximum lenght: ", LENGTH)

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
        
    
    print(generated_doc)
    print("Word count: ", len(generated_doc))
        
        
        
        
        