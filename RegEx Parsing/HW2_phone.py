# -*- coding: utf-8 -*-
import re
import argparse
#Parsing the input/output file name arguments from the terminal
#parser = argparse.ArgumentParser()
#parser.add_argument("--input", help="name of input file")
#parser.add_argument("--output", help="name of output file")
#args = parser.parse_args()

#common things that can't preceed a phone number =; fax:? ; §; digits
notbefore = "((?<!(= ))(?<!(=))(?<!(fax ))(?<!(fax: ))(?<!(§ ))(?<!(§))(?<!(\d))(?<!(\())(?<!(/)))"
#1 and 2 has to be followed by certain chars to avoid dates like 1995-1996
starting1 = "(1|2)( |\)|-|/|\\|\.)" 
#refactoring what can be in the inside of the number
inner = "(\d|\(|\)| |-|/|\.|\+)"
#longer numbers can't start with any number
longer = notbefore+"(("+starting1+"|0|\+|\()"+inner+"{12,16}\d{2}\\b)"

shorter = notbefore+"(("+starting1+"|0|[3-9]|\+|\()"+inner+"{8,13}\d{2}\\b)"
#shortest one can't start with paranthesis
shortest = notbefore+"(("+starting1+"|0|[3-9]|\+)"+inner+"{4,8}\d{2}\\b)"

#compiling the regex
regex = r"("+longer+"|"+shorter+"|"+shortest+")"

h = re.compile(regex, re.IGNORECASE)

#opening input output files and writing the results into them

#outputfile = open(args.output+"(short).txt", 'w')
#outputfile2 = open(args.output+"(long).txt", 'w')
outputfile = open('workfile.txt', 'w')
outputfile2 = open('workfile2.txt', 'w')
#with open("args.input.txt", "r") as ins:
with open("all-OANC.txt", "r") as inputfile:
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

