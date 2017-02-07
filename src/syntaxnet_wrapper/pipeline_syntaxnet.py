# -*- coding: utf-8 -*-

from tokenizer_ru import create_tokenizer_ru
from sentence_splitter import SentenceSplitter


class PipelineSyntaxNet(object):
    def __init__(self):
        self.word_tokeniser_ = create_tokenizer_ru() 
        self.sent_splitter_ = SentenceSplitter()
    
    def process(self, text):
        tokens = list(self.word_tokeniser_.span_tokenize(text))
        sents = self.sent_splitter_.process(text, tokens)
        
        return sents


#text = u'Мама мыла раму "3.5". «Дом», который - построил Джек... Биссектриса -- это kingsbounty@gmail.com http://yandex.ru'
text = u'Мама мыла раму. Дом, который - построил Джек...'

ppl = PipelineSyntaxNet()
result = ppl.process(text)

for s in result:
    for w in s:
        print w, text[w.begin : w.end]
    print '------------'
