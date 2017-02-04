import re
myfile = open('all-OANC.txt', 'r')
outputfile = open('workfile', 'w')

text = myfile.read().replace('\n', ' ')

numty = "twenty|thirtyforty|fifty|sixty|seventy|eighty|ninety"
num = "a|one|two|t[h\']ree|four|five|six|seven|eight|nine|ten|eleven|twelve|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen"

#seventy(or numbers) dollars optional cents amount
letters = "("+numty+")?( |-)?(" + num +")?( |-)?(hun[d\']red|thousand)?(million|billion)?( |-)?([1-9][0-9]*[ ,.]?[0-9]*)?( |-)?(dollars?)(("+numty+")?( |-)?(and )?(" + num +")?([1-9][0-9]*)?( |-)?cents?)?"
#dollarsign and the following value w cents
dollarsign = "(\$ ?\d+[ ,.]?\d*)"
#only values ending with cents
cents = "(("+numty+")?( |-)?(" + num +")|([1-9][0-9]*))( |-)?cents?" 


regex = r"("+letters+"|"+dollarsign+"|"+cents+")"

matches = re.findall(regex, text, flags=re.IGNORECASE)

#print matches
for match in matches:
    #print(match[0])
    outputfile.write(match[0] + "\n")

outputfile.close()
myfile.close()

