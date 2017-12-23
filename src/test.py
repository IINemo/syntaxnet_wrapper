# -*- coding: utf-8 -*-

from syntaxnet_wrapper import ProcessorSyntaxNet
from syntaxnet_wrapper import PipelineSyntaxNet


def print_result(result):
    for sent in result:
        for word in sent:
            print(word)
        print("")


if __name__ == '__main__':
    host = 'localhost'
    port = 8111
    text = 'Мама мыла раму. Дом, который построил Джек.'
    proc = PipelineSyntaxNet(host, port)
    result = proc.process(text)

    print_result(result)

    # import sys
    # import argparse
    #
    # parser = argparse.ArgumentParser(description = 'Wrapper tester.')
    #
    # parser.add_argument('--host',
    #                     required = True,
    #                     help = 'Host with SyntaxNet server.')
    # parser.add_argument('--port',
    #                     required = True,
    #                     help = 'SyntaxNet server port.',
    #                     default = 8111)
    # parser.add_argument('--proc_type',
    #                     required = True,
    #                     help = '"proc" - processor or "ppl" - pipeline')
    # args = parser.parse_args()
    #
    # text = sys.stdin.read().strip()
    #
    # if args.proc_type == 'proc':
    #     proc = ProcessorSyntaxNet(args.host, int(args.port))
    #     result = proc.parse(text)
    #     print_result(result)
    #
    # elif args.proc_type == 'ppl':
    #     ppl = PipelineSyntaxNet(args.host, int(args.port))
    #     result = ppl.process(text)
    #     print_result(result)
