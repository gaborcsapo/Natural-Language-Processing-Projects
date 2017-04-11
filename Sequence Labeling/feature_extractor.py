# -*- coding: utf-8 -*-
"""
@author: Gabor Csapo gc1569
"""
import copy
from nltk.stem import SnowballStemmer

class Extractor:
    def __init__(self):  
        self.empty()
        self.tags = ['=', 'POS=', 'BIO=']
        self.stemmer = SnowballStemmer("english")
    
    #emptying stored values when working on new file
    def empty(self):
        self.cache = {'prev2': {}, 'prev1': {}, 'next2': {}, 'next1': {}, 'current': {}}
        
    def extract(self, line, file, mytags, BIO):
        
        self.tags = mytags
        positions = [['prev1','prev2'],['next1','next2']]
        output = ''
        #moving everything down in the line by one
        self.cache['prev2'] = copy.deepcopy(self.cache['prev1'])
        self.cache['prev1'] = copy.deepcopy(self.cache['current'])
        self.cache['current'] = copy.deepcopy(self.cache['next1'])
        self.cache['next1'] = copy.deepcopy(self.cache['next2'])        
        #reading in the new value into next2
        if (line == None):
            self.cache['next2'] = {}
        else:
            new = line.strip().split('\t')
            for i in range(len(new)):
                self.cache['next2'][self.tags[i]] = new[i]
        
        #putting values for current into output
        current = self.cache['current']
        if (not current):
            return
        if (current['='] == '\n' or current['='] == ''):
            file.write('\n')
            return
        output += current["="] + '\t'
        output += "STEM=" + self.stemmer.stem(current["="]) + '\t'
        output += "POS=" + current["POS="] + '\t'
        output += "CAP=" + str(current["="][0].isupper()) + '\t'
        
        #putting values into output for the words before and after
        for direction in positions:
            for position in direction:
                item = self.cache[position]
                if (not item):
                    break
                if (item['='] == ''):
                    break
                if (item['POS='] == '.'):
                    break
                for tag in self.tags:
                    output += position + tag + item[tag] + '\t'
                output += position + "STEM=" + self.stemmer.stem(item['=']) + '\t'
                output += position + "CAP=" + str(item["="][0].isupper()) + '\t'
        #for the trainign we have BIO but for the test we don't
        if (BIO):
            output += current["BIO="]
        file.write(output + '\n')
    
         
		
out_test = open("test.chunk", 'w')
out_training = open("training.chunk", 'w')

extractor = Extractor()
#traingin file
with open("WSJ_02-21.pos-chunk", "r") as in_training:
    for line in in_training:
        extractor.extract(line, out_training, ['=', 'POS=', 'BIO='], True)
extractor.extract(None, out_training, ['=', 'POS=', 'BIO='], True)
out_training.write('\n')
#test file
extractor.empty()
with open("WSJ_23.pos", "r") as in_test:
    for line in in_test:
        extractor.extract(line, out_test, ['=', 'POS='], False)
extractor.extract(None, out_test, ['=', 'POS='], False)
out_test.write('\n')

           
out_test.close()
out_training.close()
in_test.close()
in_training.close()