# -*- coding: utf-8 -*-

from syntaxnet_wrapper import ProcessorSyntaxNet
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Wrapper tester.')
    
    parser.add_argument('--host', 
                        required = True, 
                        help = 'Host with syntaxnet server.')
    parser.add_argument('--port',
                        required = True,
                        help = 'Syntaxnet server port.',
                        default = 8111)
    args = parser.parse_args()
    
    proc = ProcessorSyntaxNet(args.host, int(args.port))
    
    text = sys.stdin.read().decode('utf8').strip()
    result = proc.parse(text)
    
    for sent in result:
        for word in sent:
            print word
        print
