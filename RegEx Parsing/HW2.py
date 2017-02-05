import re
import argparse
#Parsing the input/output file name arguments from the terminal
#parser = argparse.ArgumentParser()
#parser.add_argument("--input", help="name of input file")
#parser.add_argument("--output", help="name of output file")
#args = parser.parse_args()
#opening files that we parse and write into
#myfile = open(args.input, 'r')
#outputfile = open(args.output, 'w')

myfile = open('custom.txt', 'r')
outputfile = open('workfile.txt', 'w')

text = myfile.read().replace('\n', ' ')

numty = "(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)"
num = "(a|one|two|t[h\']ree|four|five|six|seven|eight|nine|ten|eleven|twelve|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)"

letternumber = "("+numty+"( |-)?"+num+"?( |-)?(hun[d\']red|thousand)?(million|billion|trillion)?|"\
               +numty+"?( |-)?"+num+"( |-)?(hun[d\']red|thousand)?(million|billion|trillion)?|"\
               +numty+"?( |-)?"+num+"?( |-)?(hun[d\']red|thousand)(million|billion|trillion)?|"\
               +numty+"?( |-)?"+num+"?( |-)?(hun[d\']red|thousand)?(\d+)?( million| billion| trillion))"


cents = "([(US)$.]?("+letternumber+"|(\d+[ ,.]?)+\d)( |-| U.S. )cents?\\b)"

dollartext = "("+letternumber+"|(\d+[ ,.]?)+\d)( |-)?dollars?\\b( |and )?"+cents+"?"

dollarsign = "((US)?\$ ?(\d+[ ,.]?)+\d)"


regex = r"("+dollartext+"|"+dollarsign+"|"+cents+")"
matches = re.findall(regex, text, flags=re.IGNORECASE)

#print matches
for match in matches:
    print(match[0])
    outputfile.write(match[0] + "\n")

outputfile.close()
myfile.close()

