import socket
from annotation import Word
from conll_format_parser import ConllFormatStreamParser
import sys


class ProcessorSyntaxNet(object):
    def __init__(self, host, port):
        self.host_ = host
        self.port_ = port
    
    def parse(self, input_text, sentences = None):
        raw_input_s = self._prepare_raw_input_for_syntaxnet(input_text, 
                                                            sentences)        
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host_, self.port_))
        sock.sendall(raw_input_s)
        raw_output_s = self._read_all_from_socket(sock)
        sock.close()

        if not raw_output_s:
            return None
        
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
        raw_input_s = u''
        if not sentences:
            raw_input_s = text + u'\n\n'
        else:
            for sent in sentences:
                line = u' '.join((text[e.begin : e.end] for e in sent))
                raw_input_s += line
                raw_input_s += u'\n'
            raw_input_s += u'\n'
        
        return raw_input_s.encode('utf8')
        
    def _read_all_from_socket(self, sock):
        buf = str()

        # try:
        #     while True:
        #         chunk = sock.recv(51200)
        #         buf += chunk
        #         if '\n\n\n' in buf:
        #             break
        # except socket.error as err:
        #     print 'Socket ERROR ERROR'
        #     print >>sys.stderr, err
        
        try:
            while True:
                data = sock.recv(51200)
                if data:
                    buf += data
                else:
                    break
        except socket.error as err:
            print >>sys.stderr, 'Err: Socket error: ', err

        return buf
  
    def _parse_conll_format(self, string):
        try:
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
        except IndexError as err:
            print >>sys.stderr, 'Err: Index error:', err
            print >>sys.stderr, '----------------------------'
            print >>sys.stderr, string
            print >>sys.stderr, '----------------------------'
            raise

