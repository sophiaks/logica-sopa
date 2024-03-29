import sys
import re
from mparser import Parser
from asm import ASM as asm_write
from aux import mprint

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

# Running the program
# RUN WILL CALL PARSEBLOCK
if len(code) == 0:
    raise Exception("Empty input")

def printChildren(children):
    print(children.children)

res = Parser.run(code) 
mprint(f"ROOT RES: {res.children}")
mprint("\n\n------------------")
mprint("---- EVALUATE ----")
mprint("------------------\n\n")

res.Evaluate()

filename_no_ext = filename.split(".")[0]
print(filename_no_ext
asm_write.createFile(filename_no_ext)

if Parser.tokenizer.next.type != 'EOF':
    raise Exception(f"Found unexpected token '{Parser.tokenizer.next.value}'")
