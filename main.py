import sys
from parser import Parser
import re


char_dict = {
    'PLUS': '+',
    'MINUS': '-',
    'DIV': '/',
    'MULT': '*',
    'OPEN_PAR': '(',
    'CLOSE_PAR': ')' 
}


def prePro(source):
    clean_code = re.sub(r"\s+","", source)
    no_comments_hashtag = re.sub('#.*', '', clean_code)

    no_comments = re.sub('//.*', '', no_comments_hashtag).strip()
    #print(f"No comments: {no_comments}")
    if no_comments != re.sub("\s*", '', no_comments):
        raise Exception("Between two numbers there must be an operand")
    return no_comments

filename = sys.argv[1]
file = open(filename, 'r')
lines =  file.readlines()
code = ''
for line in lines:
    code += prePro(line)

# print(f"Code -> {code}")

# Running the program
# RUN WILL CALL PARSEBLOCK
if len(code) == 0:
    raise Exception("Empty input")

res = Parser.run(code)
res.Evaluate()
# PARSEBLOCK -> 2 IFS
# comecou com letra separa
# DOS VERIFICA SE NAO É PALAVRA RESERVADA
#SE FOR RESERVADA - DISPARA print
#ELSE VARIAVL