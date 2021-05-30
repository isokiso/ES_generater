import numpy as np
import re
import csv
from janome.tokenizer import Tokenizer
import sys

import parser
from preprocessing import Converter
import markovify



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
    sentences = ''.join(sentences)
    
    tokenizer = Tokenizer()
    tokens = list(tokenizer.tokenize(sentences, wakati=True))
    splitted_text_list = []
    # 分かち書きされているtokensを一つずつ処理していき
    # 「。」や感嘆符でなければ、文字の後にスペース、
    # 「。」や感嘆符であれば、「'\n'」に置換
    # splitted_text_listに連結。
    # リストの要素を連結し、一つの文字列にして返します。
    for i in tokens:
        if i != '。' and i != '！' and i != '？':
            i += ' '
        elif i == '。' or i == '！' or i == '？':
            i = '\n'
        splitted_text_list.append(i)
        splitted_text_str = "".join(splitted_text_list)
    
    model = markovify.NewlineText(splitted_text_str, state_size=2)
    generated_doc = ""
    while True:
        new_sentence = re.sub(" ", "", model.make_short_sentence(100)) +"。"
        if len(generated_doc+new_sentence) > LENGTH:
            break
        generated_doc += new_sentence
        
    print(generated_doc)
    print("Word count: ", len(generated_doc))
    