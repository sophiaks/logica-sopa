import json
from logging import raiseExceptions
import sys
from tokenizer import Tokenizer, Token
from parser import Parser
from node import Node

char_dict = {
    'PLUS': '+',
    'MINUS': '-',
    'DIV': '/',
    'MULT': '*',
    'OPEN_PAR': '(',
    'CLOSE_PAR': ')' 
}

# Implementation for one line only - can be adapted for more than one line
filename = sys.argv[1]
file = open(filename, 'r')
line =  file.readlines()
first_line = line[0]

# Running the program
res = Parser.run(first_line)
print(res.Evaluate())