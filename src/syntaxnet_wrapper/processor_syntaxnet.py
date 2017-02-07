import socket
from annotation import Word
from conll_format_parser import ConllFormatStreamParser


class ProcessorSyntaxNet(object):
    def __init__(self, host, port):
        self.host_ = host
        self.port_ = port
    
    def parse(self, input_text, sentences = None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host_, self.port_))
        
        text = u''
        if not sentences:
            text = input_text + u'\n'
        else:
            for sent in sentences:
                line = u' '.join((input_text[e.begin : e.end] for e in sent))
                text += line
                text += u'\n'
        
        s.send(text.encode('utf8'))
        trees = self._read_all_from_socket(s)
        s.close()
        
        if sentences:
            for in_sent, p_sent in zip(sentences, trees):
                for in_word, p_word in zip(in_sent, p_sent):
                    p_word.begin = in_word.begin
                    p_word.end = in_word.end
        
        return trees
        
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
