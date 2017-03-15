# -*- coding: utf-8 -*-
import nltk

grammar = nltk.grammar.CFG.fromstring("""
 S -> NP VP
 VP -> VBP SBAR
 SBAR -> IN S
 S -> NP VP
 VP -> VBP PP
 NP -> NP PP
 PP -> IN NP
 NP -> DT NG
 NG -> NN
 NG -> NNS
 NP -> NNS
 NP -> DT NG
 NG -> JJ NG
 NG -> NN NN
 
 DT -> 'any'
 DT -> 'the'
 JJ -> 'habitable'
 NNS -> 'areas'
 NN -> 'border'
 NN -> 'region'
 IN -> 'in'
 VBP -> 'are'
 IN -> 'on'
 NN -> 'planet'
 VBP -> 'think'
 IN -> 'that'
 NNS -> 'Scientists'
""")

a = "Scientists think that any habitable areas on the planet are in the border region"

tokens = nltk.tokenize.word_tokenize(a)
print tokens
parser = nltk.ChartParser(grammar)
for tree in parser.parse(tokens):
     print(tree)




