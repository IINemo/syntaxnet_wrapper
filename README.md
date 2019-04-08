# Description
A Python 3 wrapper for [Google's SyntaxNet parser](https://www.tensorflow.org/tutorials/syntaxnet/).
The wrapper is considered to work with dockerized [SyntaxNet server](https://github.com/IINemo/docker-syntaxnet_rus). 
The wrapper connects to container via tcp and performs basic preparation/parsing of SyntaxNet parser results.

# Basic usage
The basic example of usage is presented in [src/test.py](https://github.com/IINemo/syntaxnet_wrapper/blob/master/src/test.py)

## 1. Using ProcessorSyntaxNet
ProcessorSyntaxNet needs tokenized and splitted text for work. It can also handle only raw unicode text, in which words are splitted by spaces.

```python
# -*- coding: utf-8 -*-

from syntaxnet_wrapper import ProcessorSyntaxNet

def print_result(result):
    for sent in result:
        for word in sent:
            print(word)
        print

host = '<myhsot>'
port = 8111 # E.g.
text = u'Мама мыла раму . Дом , который построил Джек .'

proc = ProcessorSyntaxNet(host, port)
result = proc.parse(text)
print_result(result)

```
## 2. Using PipelineSyntaxNet
The pipeline performs tokenization and sentence splitting for Russian and launches ProcessorSyntaxNet. It also supplies results with information about spans.

```python
# -*- coding: utf-8 -*-

from syntaxnet_wrapper import PipelineSyntaxNet

def print_result(result):
    for sent in result:
        for word in sent:
            print(word)
        print

host = '<myhsot>'
port = 8111 # E.g.
text = u'Мама мыла раму. Дом, который построил Джек.'

proc = PipelineSyntaxNet(host, port)
result = proc.process(text)
print_result(result)
```
