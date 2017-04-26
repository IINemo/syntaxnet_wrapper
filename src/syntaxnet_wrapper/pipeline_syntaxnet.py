# -*- coding: utf-8 -*-

from tokenizer_ru import create_tokenizer_ru
from sentence_splitter import SentenceSplitter
from processor_syntaxnet import ProcessorSyntaxNet


class PipelineSyntaxNet(object):
    def __init__(self, host, port):
        self.word_tokeniser_ = create_tokenizer_ru() 
        self.sent_splitter_ = SentenceSplitter()
        self.syntaxnet_parser_ = ProcessorSyntaxNet(host, port)
    
    def process(self, text, raw_output = False):
        tokens = list(self.word_tokeniser_.span_tokenize(text))
        sents = self.sent_splitter_.process(text, tokens)
        trees = self.syntaxnet_parser_.parse(text, sents, raw_output = raw_output)
        
        return trees
