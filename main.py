import re
import sys
import itertools
from urllib.parse import parse_qs

source = sys.argv[1]

def lexicalOptimization(source):
    return re.sub(r'(\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+', '', source)


def isNumber(num):
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
        temp_next = ''
        print("selectNext called")
        while isNumber(self.source[self.position]):
            print("Char is number")
            if (self.source[self.position + 1] == '+') or (self.source[self.position + 1] == '-'):
                print(f"Found a sign in position {self.position + 1}")
                self.next = Token('INT', int(temp_next))
                print(f"Updating next token to {self.next.value}")
            else:
                temp_next += self.source[self.position]
                print(f"Position: {self.position}, char: {self.source[self.position]}")

                self.position += 1
        if temp_next != '':    
            print("temp_next is empty")
            self.next = Token('INT', int(temp_next))
                
        if self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            print(f"Position: {self.position}, char: {self.source[self.position]}")
            self.position += 1
        elif self.source[self.position] == '-':
            print(f"Position: {self.position}, char: {self.source[self.position]}")
            self.next = Token('MINUS', '-')
            self.position += 1
        # elif self.source[self.position] == '*':
        #     self.next = Token('MULT', '*')
        #     print(f"Updating next token to {self.next}")
        # elif self.source[self.position] == '/':
        #     self.next = Token('DIV', '/')
        #     print(f"Updating next token to {self.next}")
        elif self.position > len(self.source):
            self.next = Token('EOF', '')
            print(f"Reached end of file")
        
        
            

class Parser:

    tokenizer = None

    @staticmethod
    def parseExpression():
        Parser.tokenizer.selectNext()
        print(f"Token: {Parser.tokenizer.next.type, Parser.tokenizer.next.value}")
        res = 0
        if Parser.tokenizer.next.type == 'INT':
            res = int(Parser.tokenizer.next.value)
            print("After int, selecting next")
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:
                print("Found plus or minus")
                if Parser.tokenizer.next.type == 'PLUS':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res += Parser.tokenizer.next.value
                    else: 
                        raise Exception("Syntax Error")
                if Parser.tokenizer.next.type == 'MINUS':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res -= Parser.tokenizer.next.value
                    else:
                        raise Exception("Syntax Error")
                Parser.tokenizer.selectNext()
            print(f"Res: {res}")
            return res

    # @staticmethod
    # def parseTerm(tokenizer):
    #     print("Beginning to parse expression...")
    #     token_type = tokenizer.next.type
    #     res = 0
    #     if token_type == 'INT':
    #         res = int(tokenizer.next.value)
    #         tokenizer.selectNext()
    #         while token_type in ['MULT', 'DIV']:
    #             if token_type == 'MULT':
    #                 tokenizer.selectNext()
    #                 if tokenizer.next.type == 'INT':
    #                     res *= tokenizer.next.value
    #                 else: 
    #                     raise Exception("Syntax Error")
    #             if token_type == 'DIV':
    #                 tokenizer.selectNext()
    #                 if tokenizer.next.type == 'INT':
    #                     res /= tokenizer.next.value
    #                 else:
    #                     raise Exception("Syntax Error")
    #             tokenizer.selectNext()
    #         return res
    
    def run(code):
        print("Runnning Code")
        print(".")
        print("..")
        print("...")
        Parser.tokenizer = Tokenizer(lexicalOptimization(code))
        Parser.parseExpression()


Parser.run(source)