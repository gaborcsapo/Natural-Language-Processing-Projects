# -*- coding: utf-8 -*-
"""
@author: Gabor Csapo
"""
from nltk.stem import SnowballStemmer
    
tags = ['=', 'POS=', 'BIO=']
positions = ['prev2', 'prev1', '', 'next1', 'next2']
stemmer = SnowballStemmer("english")
      
def seq_label(line, file, BIO):
    output = ''   
    #poping oldest value in quque
    queue.pop(0)
    #reading in the new value into next2
    queue.append({})
    if (line != None):
        new = line.strip().split('\t')
        for i in range(len(new)):
            queue[4][tags[i]] = new[i]
    #adding features to the file
    for pos in [2, 0, 1, 3, 4]:
        item = queue[pos]
        equality = '='
        #some special rules are required
        if (pos == 2):
            if (not item):
                return
            equality = ''
            if (item['='] == '\n' or item['='] == ''):
                file.write('\n')
                return
        elif (not item or item['='] == '' or item['POS='] == '.'):
            break
        
        output += positions[pos] + equality + item['='] + '\t'
        output += positions[pos] + "POS=" + item['POS='] + '\t'
        output += positions[pos] + "STEM=" + stemmer.stem(item['=']) + '\t'
        output += positions[pos] + "CAP=" + str(item["="][0].isupper()) + '\t'
        if (BIO and pos != 2):
            output += positions[pos] + "BIO=" + item['BIO='] + '\t'
    if (BIO):
        output += queue[2]['BIO=']
    file.write(output + '\n')   
        

#read and tag training file
queue = [None, None, None, None, None]
train_output = open("training.chunk", 'w')
with open("WSJ_02-21.pos-chunk", "r") as train_input:
    for line in train_input:
        seq_label(line, train_output, True)
seq_label(None, train_output, True)
train_output.write('\n')
train_output.close()
train_input.close()

#read and tag test file
queue = [None, None, None, None, None]
test_output = open("test.chunk", 'w')
with open("WSJ_23.pos", "r") as test_input:
    for line in test_input:
        seq_label(line, test_output, False)
seq_label(None, test_output, False)
test_output.write('\n')
test_output.close()
test_input.close()