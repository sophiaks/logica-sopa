from lib2to3.pgen2.tokenize import tokenize
import re
import sys
import itertools
from urllib.parse import parse_qs

source = sys.argv[1]

def lexicalOptimization(source):
    '''
    Removes all blank spaces before parsing.
    '''
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
        self.first = True

    def selectNext(self):
        temp_next = ''
        
        if self.position >= len(self.source):
            self.next = Token('EOF', '')
            quit()
        
        while isNumber(self.source[self.position]):
            print(f"char: {self.source[self.position]}")
            if (self.position != len(self.source) - 1):
                if (self.source[self.position + 1] == '+') or (self.source[self.position + 1] == '-'):
                    temp_next += self.source[self.position]
                    self.next = Token('INT', int(temp_next))
                    self.first = False
                    self.position += 1
                    temp_next == ''
                    return
                
                else:
                    temp_next += self.source[self.position]

            else: 
                temp_next += self.source[self.position]
                self.next = Token('INT', int(temp_next))
                return

            self.position += 1

        if temp_next != '':
            self.next = Token('INT', int(temp_next))
            self.position += 1
            print(f"position: {self.position}")
                
        if self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            self.position += 1
            print(f"position: {self.position}")

        if self.source[self.position] == '*':
            print("Found *")
            self.next = Token('MULT', '*')
            self.position += 1
            print(f"position: {self.position}")


        if self.source[self.position] == '/':
            self.next = Token('DIV', '/')
            self.position += 1
            print(f"position: {self.position}")




class Parser:

    tokenizer = None
    res = 0

    @staticmethod
    def parseTerm():
        print("Inside parseTerm")
        if Parser.tokenizer.first:
            Parser.tokenizer.selectNext()
            print(f"First token is: {Parser.tokenizer.next.value}")
            res = Parser.tokenizer.next.value
        
        if Parser.tokenizer.next.type == 'INT':
            res = int(Parser.tokenizer.next.value)
            print(f"Res: {res}")
            print(f"Position: {Parser.tokenizer.position}")
            Parser.tokenizer.selectNext()
            print(f"Token: {Parser.tokenizer.next.value}")
            print(f"Token: {Parser.tokenizer.next.value}")
            while Parser.tokenizer.next.type in ['DIV', 'MULT']:
                if Parser.tokenizer.next.type == 'MULT':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res *= Parser.tokenizer.next.value
                    else: 
                        raise Exception("Syntax Error")
                if Parser.tokenizer.next.type == 'DIV':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res //= Parser.tokenizer.next.value
                    else:
                        raise Exception("Syntax Error")
                Parser.tokenizer.selectNext()
                if (Parser.tokenizer.next.type == 'EOF'):
                    return res 
            if Parser.tokenizer.next.type in ['PLUS', 'MINUS']:
                Parser.parseExpression()
            print(f"{res}")
            return res
        else:
            raise Exception(f"{Parser.tokenizer.next.value} is not an INT type")


    @staticmethod
    def parseExpression():
        if Parser.tokenizer.first:
            Parser.tokenizer.selectNext()
            res = Parser.tokenizer.next.value
        
        if Parser.tokenizer.next.type == 'INT':
            res = int(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:
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
                if (Parser.tokenizer.next.type == 'EOF'):
                    return res 
            # if Parser.tokenizer.next.type in ['DIV', 'MULT']:
            #     Parser.parseTerm()
            print(f"{res}")
            return res
        else:
            raise Exception(f"{Parser.tokenizer.next.value} is not an INT type")

    def run(code):
        Parser.tokenizer = Tokenizer(lexicalOptimization(code))
        Parser.parseTerm()


class prePro():
    @staticmethod
    def filter():
        pass

Parser.run(source)
