# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:55:15 2017
@author: Jihyun
"""
import probability
from sys import argv

def get_clean_line(line):
    return line.strip().lower().split()

def showthediff(file1, file2):
    freq = {}
    output = open('diff.txt', 'w')
    output.write("Word\tnew\tsys\n")
    count = 0
    with open(file1) as f1, open(file2) as f2:
        for line1, line2 in zip(f1, f2):
            get1, get2 = get_clean_line(line1), get_clean_line(line2)
            if len(get1) == 2 and len(get2) == 2:
                if get1[1] != get2[1]:
                    if get1[0] in freq:
                        freq[get1[0]] += 1
                    else:
                        freq[get1[0]] = 1
                    output.write(str(get1[0])+'\t'+str(get1[1])+'\t'+str(get2[1])+'\n')
                    count += 1

    print(sorted(freq.items(), key=lambda x:x[1]))
    f1.close()
    f2.close()
    output.close()

def viterbi(trainfile, testfile):
    
    output = open('jk4704-gc1569.pos', 'w')
    
    processor = probability.Probab() 
    processor.readIntoTable(trainfile)    

    with open(testfile, "r") as test: 
       
        prev = "Start/End"
        for line in test:
            line = line.strip("\n")
            if line is "":
                prev = "Start/End"
                output.write("\n")
            else:
                maxp = 0
                if line in processor.POS_opt:
                    if line.lower() in ['the','a', 'any','an','this','all']:
                        tag = 'DT'
                    elif line.lower() == "'s":
                        tag = 'POS'
                    elif line.lower() in ['by','for','in','on','at','about','with','as','of']:
                        tag = "IN"
                    elif line.lower() in ["but",'and']:
                        tag = "CC"
                    else:
                        for tag in processor.POS_opt[line]:
                            if processor.getProb(prev, tag, line) > maxp:
                                maxp = processor.getProb(prev, tag, line)
                else:
                    for tag in processor.transitions:
                        if processor.getProb(prev, tag, line) > maxp:
                            maxp = processor.getProb(prev, tag, line)
                            prev = tag

                prev = tag
                output.write(line + "\t" + tag + "\n")
                   
    output.close()
    test.close()

viterbi('train.pos', 'WSJ_23.words')
#showthediff('output.pos','WSJ_23.pos')