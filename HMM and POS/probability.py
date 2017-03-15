# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 20:10:02 2017

@author: Gabor
"""
import re

class Probab():
    def __init__(self):
        self.emissions = {}
        self.POS_opt = {}
        self.transitions = {}
        self.prevPOS = 'Start/End'
        self.unknown = {}
        self.ing = {}
        self.ly = {}
        self.s_ending = {}
        self.er = {}
        self.hyphenated = {}
        self.numbers = {}
    
    def readIntoTable(self, file):
        with open(file, "r") as inputfile:
            for line in inputfile:
                element = line.strip().split('\t')
                if (len(element) == 1):
                    element.append('Start/End')
                self.addElem(element)        
        inputfile.close()        
        self.preProcOOV()
        self.calcProb()        
        
    #adding an element to the dictionary to count its frequency
    def addElem(self, element):
        #counting words
        if (element[1] in self.emissions):
            if (element[0] in self.emissions[element[1]]):
               self.emissions[element[1]][element[0]] += 1
            else:
               self.emissions[element[1]][element[0]] = 1
        else:
           self.emissions[element[1]] = {element[0]: 1}
        
        #counting words
        if (element[0] in self.POS_opt):
            if (element[1] not in self.POS_opt[element[0]]):
               self.POS_opt[element[0]].add(element[1])
        else:
           self.POS_opt[element[0]] = {element[1]}
        
        #counting transitions
        if (self.prevPOS in self.transitions):
            if (element[1] in self.transitions[self.prevPOS]):
                self.transitions[self.prevPOS][element[1]] += 1
            else:
                self.transitions[self.prevPOS][element[1]] = 1
        else:
            self.transitions[self.prevPOS] = {element[1]: 1}
        
        self.prevPOS = element[1]
    
    #unique strategy to deal with OOV
    #words that only appear once get put into special categories
    def preProcOOV(self):        
        for tag in self.emissions:
            for word in self.emissions[tag]:
                if (self.emissions[tag][word] < 2):                 
                    if (word[-3:] == 'ing'):
                        self.addToDict(self.ing, tag)
                    elif (word[-1] == 's'):
                        self.addToDict(self.s_ending, tag)
                    elif (word[-2:] == 'ly'):
                        self.addToDict(self.ly, tag)
                    elif (word[-2:] == 'er'):
                        self.addToDict(self.er, tag)
                    elif (re.search('\d', word)):
                        self.addToDict(self.numbers, tag)
                    elif (re.search('-', word)):
                        self.addToDict(self.hyphenated, tag)
                    else:
                        self.addToDict(self.unknown, tag)             
    
    #converts all dictionaries to probability from frequency  
    def calcProb(self):       
        for dictionary in [self.emissions, self.transitions]: 
            for outer_key in dictionary:
                total = 0
                for key in dictionary[outer_key]:
                    total += dictionary[outer_key][key]
                for key in dictionary[outer_key]:
                    if total < 15:
                        total *= 100
                    dictionary[outer_key][key] = dictionary[outer_key][key]/total
        for dictionary in [self.unknown, self.ing, self.ly, self.s_ending, self.er, self.hyphenated, self.numbers]:
            total = 0
            for tag in dictionary:
                total += dictionary[tag]
            for tag in dictionary:
                dictionary[tag] = dictionary[tag]/total
    
    #get probability function, if word is unknown, gets special treatment    
    def getProb(self, prevState, state, word):
        word_prob = 0.0000001
        #word probabillity
        if (word in self.emissions[state]):
            word_prob = self.emissions[state][word]
        #out of vocab word
        elif (word[-3:] == 'ing'):
            if state in self.ing:
                word_prob = self.ing[state] 
        elif (word[-1] == 's'):
            if state in self.s_ending:
                word_prob == self.s_ending[state] 
        elif (word[-2:] == 'ly'):
            if state in self.ly:
                word_prob ==self.ly[state] 
        elif (word[-2:] == 'er'):
            if state in self.er:
                word_prob = self.er[state] 
        elif (re.search('\d', word)):
            if state in self.numbers:
                word_prob = self.numbers[state] 
        elif (re.search('-', word)):
            if state in self.hyphenated:
                word_prob = self.hyphenated[state] 
        elif (state in self.unknown):
            word_prob = self.unknown[state]
        else:
            #print("Note: unknown word <"+word+">, no special rules, its prob set to 0.0000001")
            word_prob = 0.0000001
        
        #transition probability
        if (state in self.transitions[prevState]):
            tran_prob = self.transitions[prevState][state] 
        else:
            #print(word)
            #print("Note: unknown transition from <"+prevState+"> to <"+state+">, its prob set to 0.000001")
            tran_prob = 0.000001
               
        return tran_prob * word_prob
    
    #util function to add something to a dictionary
    def addToDict(self, dictionary, tag):
        if tag in dictionary:
            dictionary[tag] += 1
        else:
            dictionary[tag] = 1