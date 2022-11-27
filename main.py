import sys
import re
from parser import Parser
from funcTable import FuncTable

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
    if no_comments != re.sub("\s*", '', no_comments):
        raise Exception("Between two numbers there must be an operand")
    return no_comments

filename = sys.argv[1]
file = open(filename, 'r')
lines =  file.readlines()
code = ''
for line in lines:
    code += prePro(line)

if len(code) == 0:
    raise Exception("Empty input")

res = Parser.run(code)
res.Evaluate(FuncTable)
