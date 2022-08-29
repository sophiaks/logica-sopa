import re
import sys
import itertools
from urllib.parse import parse_qs

source = sys.argv[1]

def isNumber(num):
    print("Checking if token is number")
    try:
        value = float(num)
        return True
    except ValueError:
        return False

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        token = self.source[self.position]
        temp_next = ""
        if isNumber(token):
            if self.source[self.position + 1] == '+' or self.source[self.position + 1] == '-':
                self.next = Token('INT', int(temp_next))
                print(f"Updating next token to {self.next}")
            else:
                temp_next += token
                print(f"Updating temp token to {temp_next}")
        elif token == '+':
            self.next = Token('PLUS', '+')
            print(f"Updating next token to {self.next}")
        elif token == '-':
            self.next = Token('MINUS', '-')
            print(f"Updating next token to {self.next}")
        elif self.position > len(self.source):
            self.next = Token('EOF', '')
            print(f"Reached end of file")
        self.position += 1
            

class Parser:
    @staticmethod
    def parseExpression(tokenizer):
        print("Beginning to parse expression...")
        token_type = tokenizer.next.type
        res = 0
        if token_type == 'INT':
            res = int(tokenizer.next)
            tokenizer.selectNext()
            while token_type in ['MINUS', 'PLUS']:
                if token_type == 'PLUS':
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'INT':
                        res += tokenizer.next.value
                    else: 
                        raise Exception("Syntax Error")
                if token_type == 'MINUS':
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'INT':
                        res -= tokenizer.next.value
                    else:
                        raise Exception("Syntax Error")
                tokenizer.selectNext()
            return res
    
    def run(code):
        print("Runnning Code")
        Parser.tokenizer = Tokenizer(code)
        Parser.parseExpression(Parser.tokenizer)


Parser.run(source)