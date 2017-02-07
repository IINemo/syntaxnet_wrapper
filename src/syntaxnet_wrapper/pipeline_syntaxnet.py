# -*- coding: utf-8 -*-

from tokenizer_ru import create_tokenizer_ru
from sentence_splitter import SentenceSplitter
from processor_syntaxnet import ProcessorSyntaxNet


class PipelineSyntaxNet(object):
    def __init__(self, host, port):
        self.word_tokeniser_ = create_tokenizer_ru() 
        self.sent_splitter_ = SentenceSplitter()
        self.syntaxnet_parser_ = ProcessorSyntaxNet(host, port)
    
    def process(self, text):
        tokens = list(self.word_tokeniser_.span_tokenize(text))
        sents = self.sent_splitter_.process(text, tokens)
        trees = self.syntaxnet_parser_.parse(text, sents)
        
        return trees


#text = u'Мама мыла раму "3.5". «Дом», который - построил Джек... Биссектриса -- это kingsbounty@gmail.com http://yandex.ru'
text = u'Мама мыла раму. Дом, который - построил Джек...'

ppl = PipelineSyntaxNet('exn5.isa.ru', 8111)
result = ppl.process(text)

for s in result:
    for w in s:
        print w, text[w.begin : w.end]
    print '------------'
