# -*- coding: utf-8 -*-

import socket
from StringIO import StringIO


class ConllFormatSentenceParser(object):
    def __init__(self, string_io):
        super(ConllFormatSentenceParser, self).__init__()
        self.string_ = string_io
        self.stop_ = False
        
    def __iter__(self):
        return self
    
    def next(self):
        if not self.stop_:
            line = self.string_.readline().rstrip('\n')
            if not line:
                self.stop_ = True
            else:
                return line.strip().split('\t')
        
        raise StopIteration()


class ConllFormatStreamParser(object):
    def __init__(self, string):
        super(ConllFormatStreamParser, self).__init__()
        self.string_io_ = StringIO(string)
        self.stop_ = False
        
    def __iter__(self):
        return self
    
    def next(self):
        if not self.stop_:
            sent_parser = ConllFormatSentenceParser(self.string_io_)
            result = list(sent_parser)
            if not result:
                self.stop_ = True
            else:
                return result
            
        raise StopIteration()


class Word(object):
    def __init__(self, pos_tag = u'', morph = u'', word_form = u'', 
                 parent = -1, link_name = u''):
        super(Word, self).__init__()
        
        self.pos_tag = pos_tag
        self.morph = morph
        self.word_form = word_form
        self.parent = parent
        self.link_name = link_name
    
    def __unicode__(self):
        return u'word_form: {} pos_tag: {} morph: {} parent {} link_name: {}'.format(self.word_form,
                                                                                     self.pos_tag,
                                                                                     self.morph,
                                                                                     self.parent,
                                                                                     self.link_name)
    def __str__(self):
        return self.__unicode__().encode('utf8')


class ProcessorSyntaxNet(object):
    def __init__(self, host, port):
        self.host_ = host
        self.port_ = port
    
    def parse(self, text):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host_, self.port_))
        
        s.send((text + u'\n').encode('utf8'))
        reply = self._read_all_from_socket(s)
        s.close()
        
        return reply
        
    def _read_all_from_socket(self, sock):
        buf = str()

        while True:
            data = sock.recv(1024)
            if data:
                buf += data
            else:
                break
        
        return self._parse_conll_format(buf)
  
    def _parse_conll_format(self, string):
        result = list()
        for sent in ConllFormatStreamParser(string):
            new_sent = list()
            for word in sent:
                new_word = Word(word_form = word[1].decode('utf8'), 
                                pos_tag = word[3].decode('utf8'),
                                morph = word[5].decode('utf8'),
                                parent = int(word[6]) - 1,
                                link_name = word[7].decode('utf8'))
                new_sent.append(new_word)
            result.append(new_sent)
        
        return result
    
    
text = u'косил косой косой косой .'
proc = ProcessorSyntaxNet('exn5.isa.ru', 8111)
reply = proc.parse(text)

for sent in reply:
    for word in sent:
        print word
    print

