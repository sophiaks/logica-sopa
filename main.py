import re
import sys
import itertools
from urllib.parse import parse_qs

source = sys.argv[1]

def prePro(source):
    #clean_code = re.sub(r'(\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+', '', source)
    clean_code = re.sub("\s*(\W)\s*",r"\1", source)
    no_comments_hashtag = re.sub('#.*', '', clean_code)
    no_comments = re.sub('//.*', '', no_comments_hashtag)
    if no_comments != re.sub("\s*", '', no_comments):
        raise Exception("Between two numbers there must be an operand")
    if len(no_comments) == 0:
        raise Exception("Empty input")
    return no_comments

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
            # if character is a number
            if (self.position != len(self.source) - 1):
                # if not EOF
                char = self.source[self.position + 1]
                if (char == '+') or (char == '-') or (char =='*') or char == '/':
                    # if next char is an operator
                    temp_next += self.source[self.position]
                    # concatenates number
                    self.next = Token('INT', int(temp_next))
                    self.first = False
                    temp_next == ''
                    self.position += 1
                    # returns token, empties temp_next and increases position
                    return
                
                else:
                    temp_next += self.source[self.position]

            else: 
                temp_next += self.source[self.position]
                self.next = Token('INT', int(temp_next))
                return

            self.position += 1
            
        if temp_next == ' ':
            raise Exception("Cannot have spaces between numbers")
        
        if temp_next != '':
            self.next = Token('INT', int(temp_next))
            self.position += 1
                
        if self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            self.position += 1

        if self.source[self.position] == '-':
            self.next = Token('MINUS', '-')
            self.position += 1

        if self.source[self.position] == '*':
            self.next = Token('MULT', '*')
            self.position += 1 
         
        if self.source[self.position] == '/':
            self.next = Token('DIV', '/')
            self.position += 1

            

class Parser:

    tokenizer = None
    res = 0


    @staticmethod
    def parseExpression():
        if Parser.tokenizer.first:
            Parser.tokenizer.selectNext()
            res = Parser.tokenizer.next.value
        if Parser.tokenizer.next.type == 'INT':
            res = Parser.parseTerm()
            while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:
                if Parser.tokenizer.next.type == 'PLUS':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res += Parser.parseTerm()
                    else: 
                        raise Exception("Syntax Error")
                if Parser.tokenizer.next.type == 'MINUS':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res -= Parser.parseTerm()
                    else:
                        raise Exception("Syntax Error")
            
            print(res)
            return res
        else:
            raise Exception(f"{Parser.tokenizer.next.value} is not an INT type")

    @staticmethod
    def parseTerm():
        if Parser.tokenizer.next.type == 'INT':
            res = int(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
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
            return res
        else:
            raise Exception(f"{Parser.tokenizer.next.value} is not an INT type")

    
    
    def run(code):
        Parser.tokenizer = Tokenizer(prePro(code))
        Parser.parseExpression()


Parser.run(source)
