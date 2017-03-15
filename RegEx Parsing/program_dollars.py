import re
import argparse
#Parsing the input/output file name arguments from the terminal
parser = argparse.ArgumentParser()
parser.add_argument("input", help="name of input file without .txt")
parser.add_argument("output", help="name of output file without .txt")
args = parser.parse_args()
if (args.output == None or args.input == None):
    print "incorrect arguments. Type python program_dollars.py <name of input file without .txt> <name of output file without .txt>"
    exit();

#most efficient way of searching for numbers writen with characters
letternumber = "((e(?:leven|ight(?:een|y)?)|"\
                "t(?:w(?:o|e(?:lve|nty))|h(?:irt(?:een|y)|ousand|ree)|en|rillion)|"\
                "f(?:o(?:ur(?:teen)?|rty)|i(?:ft(?:een|y)|ve))|"\
                "s(?:ix(?:t(?:een|y))?|even(?:t(?:een|y))?)|"\
                "nine(?:t(?:een|y))?|"\
                "one|"\
                "hundred|"\
                "[mb]illion)( |-)?)+"

words = "a? few |several |half a |quarter of |many " 
#searching for digits with every form of decimal separators
digit = "\d+([ ,\.-]?\d+){0,3}"
#expressions that only have cents includes corner cases such as US$ .38 cents
cents = "((\\bUS ?|U\.S\. ?|$ ?| ?\.)*("+letternumber+"|"+digit+")( |-| U.S. )cents?\\b)"
#expressions that contain "dollar" with option $ or cents expression
dollartext = "(\\bUS ?|\$ ?|"+words+")*("+letternumber+"|"+digit+")( |-)?dollars?\\b( |and )?"+cents+"?"
#expressions containing $ signs
dollarsign = "(?<!(\$))(\\bUS ?)?\$ ?"+digit+"( hundred| thousand| million| billion| trillion)?"
#expressions saying things like millions of dollars
ofdollars = "((m|b|tr)illions|thousands|hundreds) of dollars"

#compiling the regex
regex = r"("+dollartext+"|"+dollarsign+"|"+cents+"|"+ofdollars+")"
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
                query = match[0].replace("$", "\$").replace("(", "\(").replace(")", "\)").replace(".", "\.").replace("+", "\+").replace("[", "\[").replace("]", "\]")
                outputfile.write( match[0] + "\n")
                bracketed = re.sub(r'('+ query +')', r'[\1]', bracketed)
            #print bracketed
            #print "\n"
            outputfile2.write(bracketed + "\n")
           
outputfile.close()
outputfile2.close()
inputfile.close()

