import re
import argparse
#Parsing the input/output file name arguments from the terminal
#parser = argparse.ArgumentParser()
#parser.add_argument("--input", help="name of input file")
#parser.add_argument("--output", help="name of output file")
#args = parser.parse_args()



country = "(\+?1\s*([.-]\s*)?)?"



phone = "("+country+"((\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]‌​)\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*([.-]\s*)?)?([2-9]1[02-‌​9]|[2-9][02-9]1|[2-9][02-9]{2})\s*([.-]\s*)?([0-9]{4})"



#compiling the regex
regex = r"("+phone+")"
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
            for match in matches:
                query = match[0].replace("$", "\$");
                outputfile.write( match[0] + "\n")
                bracketed = re.sub(r'('+ query +')', r'[\1]', line)
            #print bracketed
            #print "\n"
            outputfile2.write(bracketed + "\n")
           
outputfile.close()
outputfile2.close()
inputfile.close()

