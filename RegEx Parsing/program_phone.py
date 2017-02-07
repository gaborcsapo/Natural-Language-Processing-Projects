# -*- coding: utf-8 -*-
import re
import argparse
#Parsing the input/output file name arguments from the terminal
parser = argparse.ArgumentParser()
parser.add_argument("input", help="name of input file without .txt")
parser.add_argument("output", help="name of output file without .txt")
args = parser.parse_args()
if (args.output == None or args.input == None):
    print "incorrect arguments. Type python HW2_phone.py <name of input file without .txt> <name of output file without .txt>"
    exit();

#common things that can't preceed a phone number =; fax:? ; §; digits
notbefore = "((?<!(= ))(?<!(=))(?<!(fax ))(?<!(fax: ))(?<!(§ ))(?<!(§))(?<!(\d))(?<!(\())(?<!(/)))"
#1 and 2 has to be followed by certain chars to avoid dates like 1995-1996
starting1 = "((1|2)( |\)|-|/))|0( |\)|-|/|\d)|\+|\(\d{1,4}\)" 
#refactoring what can be in the inside of the number when the region code and country code is typed
filler = "(\d|\(\d{1,3}\)| |-|/|\.|\+)"
#the second part of the inside needs at least 7 numbers including the beginning and the ending
inner = "\d{3}(\(|\)| |-|/|\.)?\d{2}(\(|\)| |-|/|( |\)|-|/)\.)?\d{2}"
#longer numbers can't start with any number
longer = notbefore+"(("+starting1+")"+filler+"{5,9}"+inner+"\\b)"

shorter = notbefore+"(("+starting1+"|[3-9]( |\)|-|/|\d))"+filler+"{0,5}"+inner+"\\b)"

#compiling the regex
regex = r"("+longer+"|"+shorter+")"

print regex

h = re.compile(regex, re.IGNORECASE)

#opening input output files and writing the results into them

outputfile = open(args.output+"_single.txt", 'w')
outputfile2 = open(args.output+".txt", 'w')
#outputfile = open('workfile.txt', 'w')
#outputfile2 = open('workfile2.txt', 'w')
with open(args.input+".txt", "r") as inputfile:
#with open("all-OANC.txt", "r") as inputfile:
#with open("custom.txt", "r") as inputfile:
    for line in inputfile:
       matches = h.findall(line)
       if (len(matches) != 0):
            bracketed = line
            for match in matches:
                query = match[0].replace("(", "\(").replace(")", "\)").replace(".", "\.").replace("+", "\+").replace("[", "\[").replace("]", "\]")
                outputfile.write( match[0] + "\n")
                bracketed = re.sub(r'('+ query +')', r'[\1]', bracketed)
            #print bracketed
            #print "\n"
            outputfile2.write(bracketed + "\n")
           
outputfile.close()
outputfile2.close()
inputfile.close()

