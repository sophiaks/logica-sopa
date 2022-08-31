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
        self.first = True

    def selectNext(self):
        print(f"POS: {self.position}; value: {self.source[self.position]}")
        temp_next = ''
        
        print(f"self.pos = {self.position}; len of source: {len(self.source)}")
        if self.position >= len(self.source):
            self.next = Token('EOF', '')
            print(f"Reached end of file")
            quit()
        
        while isNumber(self.source[self.position]):
            print(f"POS: {self.position}; value: {self.source[self.position]}")
            if (self.position != len(self.source) - 1):
                if (self.source[self.position + 1] == '+') or (self.source[self.position + 1] == '-'):
                    print(f"POS: {self.position}; value: {self.source[self.position]}")
                    temp_next += self.source[self.position]
                    self.next = Token('INT', int(temp_next))
                    self.first = False
                    print(f"self.next = {self.next.value}")
                    self.position += 1
                    temp_next == ''
                    return
                
                else:
                    print(f"POS: {self.position}; value: {self.source[self.position]}")
                    temp_next += self.source[self.position]
                    print(f"temp_next = {temp_next}")

            else: 
                temp_next += self.source[self.position]
                self.next = Token('INT', int(temp_next))
                return

            self.position += 1

        if temp_next != '':
            print(f"POS: {self.position}; value: {self.source[self.position]}")
            self.next = Token('INT', int(temp_next))
            self.position += 1
                
        if self.source[self.position] == '+':
            print(f"Position: {self.position}, POSITIVO")
            self.next = Token('PLUS', '+')
            self.position += 1


        if self.source[self.position] == '-':
            print(f"Position: {self.position}, NEGATIVO")
            self.next = Token('MINUS', '-')
            self.position += 1

            

class Parser:

    tokenizer = None
    res = 0

    @staticmethod
    def parseExpression():
        if Parser.tokenizer.first:
            Parser.tokenizer.selectNext()
            print(f"First token read: {Parser.tokenizer.next.value}")
            res = Parser.tokenizer.next.value
            print(res)
        else:
            print("Not first token")
        if Parser.tokenizer.next.type == 'INT':
            print("Exited func")
            res = int(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:
                if Parser.tokenizer.next.type == 'PLUS':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res += Parser.tokenizer.next.value
                        print(res)
                    else: 
                        raise Exception("Syntax Error")
                if Parser.tokenizer.next.type == 'MINUS':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'INT':
                        res -= Parser.tokenizer.next.value
                        print(res)
                    else:
                        raise Exception("Syntax Error")
                Parser.tokenizer.selectNext()
                if (Parser.tokenizer.next.type == 'EOF'):
                    return res 
            print(f"{res}")
            return res
        else:
            print(Parser.tokenizer.position)
            raise Exception(f"{Parser.tokenizer.next.value} is not an INT type")

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
        Parser.tokenizer = Tokenizer(lexicalOptimization(code))
        Parser.parseExpression()


Parser.run(source)
