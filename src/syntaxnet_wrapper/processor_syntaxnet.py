import socket
from .annotation import Word
from .conll_format_parser import ConllFormatStreamParser
import sys


class ProcessorSyntaxNet(object):
    def __init__(self, host, port):
        self.host_ = host
        self.port_ = port
    
    def parse(self, input_text, sentences = None, raw_output = False):
        raw_input_s = self._prepare_raw_input_for_syntaxnet(input_text, 
                                                            sentences)        
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host_, self.port_))
        sock.sendall(raw_input_s)
        raw_output_s = self._read_all_from_socket(sock)
        sock.close()

        if not raw_output_s:
            return None
        
        if raw_output:
            return raw_output_s

        trees = self._parse_conll_format(raw_output_s)
        
        if sentences:
            self._fill_spans_in_trees(sentences, trees)
        
        return trees
    
    def _fill_spans_in_trees(self, sentences, trees):
        for in_sent, p_sent in zip(sentences, trees):
            for in_word, p_word in zip(in_sent, p_sent):
                p_word.begin = in_word.begin
                p_word.end = in_word.end
    
    def _prepare_raw_input_for_syntaxnet(self, text, sentences):
        raw_input_s = ''
        if not sentences:
            raw_input_s = text + '\n\n'
        else:
            for sent in sentences:
                line = ' '.join((text[e.begin : e.end] for e in sent))
                raw_input_s += line
                raw_input_s += '\n'
            raw_input_s += '\n'
        
        return raw_input_s.encode('utf-8')
        
    def _read_all_from_socket(self, sock):
        buf = str()
        
        try:
            while True:
                data = sock.recv(51200)
                if data:
                    buf += data.decode('utf-8') #"".join(map(chr, data))
                else:
                    break
        except socket.error as err:
            print('Err: Socket error: ', err, file=sys.stderr)

        return buf
  
    def _parse_conll_format(self, string):
        try:
            result = list()
            for sent in ConllFormatStreamParser(string):
                new_sent = list()
                for word in sent:
                    new_word = Word(word_form = word[1], 
                                    pos_tag = word[3],
                                    morph = word[5],
                                    parent = int(word[6]) - 1,
                                    link_name = word[7])
                    new_sent.append(new_word)
                result.append(new_sent)
            
            return result
        except IndexError as err:
            print('Err: Index error:', err, file=sys.stderr)
            print('----------------------------', file=sys.stderr)
            print(string, file=sys.stderr)
            print('----------------------------', file=sys.stderr)
            raise

