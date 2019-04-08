from .annotation import Span
from nltk.tokenize.punkt import PunktSentenceTokenizer


class SentenceSplitter(object):
    def __init__(self):
        super(SentenceSplitter, self).__init__()
        self.sent_tokeniser_ = PunktSentenceTokenizer()
    
    def process(self, text, tokens):
        token_strs = [text[e[0] : e[1]] for e in tokens]
        
        sents = self.sent_tokeniser_.sentences_from_tokens(token_strs)
        curr = 0
        res_sents = list()
        for sent in sents:
            res_sents.append([Span(begin = e[0], end = e[1]) 
                              for e in tokens[curr : curr + len(sent)]])
            curr += len(sent)
        
        return res_sents
    