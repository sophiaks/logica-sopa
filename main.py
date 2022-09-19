import json
from logging import raiseExceptions
import readline
import sys
from tokenizer import Tokenizer, Token
from parser import Parser
import pandas as pd
from node import Node

char_dict = {
    'PLUS': '+',
    'MINUS': '-',
    'DIV': '/',
    'MULT': '*',
    'OPEN_PAR': '(',
    'CLOSE_PAR': ')' 
}

#source = sys.argv[1]
filename = sys.argv[1]

file = open(filename, 'r')

# Implementation for one line only - can be adapted for more than one line
line =  file.readlines()
first_line = line[0]
# with open(file) as json_file:
#     data = json.load(json_file)

#print(f"data: {data}")

res = Parser.run(first_line)
print(res.Evaluate())