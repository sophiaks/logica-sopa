from logging import raiseExceptions
import re
import sys

char_dict = {
    'PLUS': '+',
    'MINUS': '-',
    'DIV': '/',
    'MULT': '*',
    'OPEN_PAR': '(',
    'CLOSE_PAR': ')' 
}

source = sys.argv[1]

def prePro(source):
    #clean_code = re.sub(r'(\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+', '', source)
    clean_code = re.sub("\s*(\W)\s*",r"\1", source)
    no_comments_hashtag = re.sub('#.*', '', clean_code)
    no_comments = re.sub('//.*', '', no_comments_hashtag).strip()
    #print(no_comments)
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
        
        if self.position == 0:
            self.first = False
        

        if self.position >= len(self.source):
            self.next = Token('EOF', '')
            return self.next
        
        # print(f'Token: {self.source[self.position]}')
        # print(f'Position: {self.position}')
        
        temp_next = ''

        if isNumber(self.source[self.position]):
            temp_next = ''
            while isNumber(self.source[self.position]):
                temp_next += self.source[self.position]
                # print(f'Temp next: {temp_next}')
                # concatenates number
                self.position += 1
                # If reached end of file
                if self.position >= len(self.source):
                    break
            self.next = Token('INT', int(temp_next))
            #self.position += 1
            return
                
        # if temp_next != '':
        #     self.next = Token('INT', int(temp_next))
        #     self.position += 1
        #     print(f"selectNext dps de int: pod = {self.position}")
        #     return self.next

        if self.source[self.position] == ")":
            self.next = Token('CLOSE_PAR', ")")
            self.position += 1
            return self.next   
                
        elif self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            self.position += 1
            return self.next

        elif self.source[self.position] == '-':
            self.next = Token('MINUS', '-')
            self.position += 1
            return self.next

        elif self.source[self.position] == '*':
            self.next = Token('MULT', '*')
            self.position += 1
            return self.next
         
        elif self.source[self.position] == '/':
            self.next = Token('DIV', '/')
            self.position += 1
            return self.next

        elif self.source[self.position] == '(':
            self.next = Token('OPEN_PAR', '(')
            self.position += 1
            return self.next

        

        

class Parser:

    tokenizer = None
    res = 0
    open_par = False

    @staticmethod
    def parseExpression():
        #print(f"Position: {Parser.tokenizer.position}")
        # print("Aqui já tá errado (pos deveria ser 1)")
        # print(f"Current status (parseExpression): next = {Parser.tokenizer.next.value}; current token: {Parser.tokenizer.next.type}; pos: {Parser.tokenizer.position}")
        res = Parser.parseTerm()
        # print(f"Return from parseTerm (inside parseExpression): {res} // current token: {Parser.tokenizer.next.type} ")
        # print(f"Current token: {Parser.tokenizer.next.value}")

        while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:
            # print("Inside MINUS, PLUS")
            if Parser.tokenizer.next.type == 'PLUS':
                Parser.tokenizer.selectNext()
                res += Parser.parseTerm()
                # print(f"After parseTerm (inside parseEx): {Parser.tokenizer.next.value}")
                if Parser.tokenizer.next.value == ')' and Parser.open_par is False:
                    raise Exception("Closed par without opening")
            elif Parser.tokenizer.next.type == 'MINUS':
                Parser.tokenizer.selectNext()
                res -= Parser.parseTerm()
                # print(f"After parseTerm (inside parseEx): {Parser.tokenizer.next.value}")
        # print(f"Did not find + or -, returning // current token: {Parser.tokenizer.next.type}")
        return res
        
    @staticmethod
    def parseTerm():
        #print(f"Current status (parseTerm): next = {Parser.tokenizer.next.value};")
        res = Parser.parseFactor()
        #breakpoint()
        # print(f"parseFactor returned {res} // position: {Parser.tokenizer.position} // next: {Parser.tokenizer.next.value}")

        while Parser.tokenizer.next.type in ['MULT', 'DIV']:
            if Parser.tokenizer.next.type == 'MULT':
                # print("Found *")
                Parser.tokenizer.selectNext()
                res *= Parser.parseFactor()
                
            if Parser.tokenizer.next.type == 'DIV':
                # print("Found /")
                Parser.tokenizer.selectNext()
                res //= Parser.parseFactor()

        # print(f"parseTerm returned {res}")

        return res

    @staticmethod
    def parseFactor():
        # print(f"Current status (parseFactor): next = {Parser.tokenizer.next.value};")
        if Parser.tokenizer.next.type == 'INT':
            res = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == 'MINUS':
            # print("Found MINUS")
            # print("Selecting next")
            Parser.tokenizer.selectNext()
            # print("Calling parseFactor")
            res = -Parser.parseFactor()

        elif Parser.tokenizer.next.type == 'PLUS':
            # print("Found PLUS")
            # print("Selecting next")
            Parser.tokenizer.selectNext()
            # print("Calling parseFactor")
            res = Parser.parseFactor()

        elif Parser.tokenizer.next.type == 'OPEN_PAR':
            # print("Opened parenthesis")
            Parser.open_par = True
            Parser.tokenizer.selectNext()
            # print("Calling parseExpression()")
            res = Parser.parseExpression()
            # print(f"Exited parseExpression() -> next = {Parser.tokenizer.next.type}")
            
            if Parser.tokenizer.next.type != 'CLOSE_PAR':
                #print(Parser.tokenizer.source[Parser.tokenizer.position - 1])
                #if Parser.tokenizer.source[Parser.tokenizer.position - 1] == ')' or Parser.tokenizer.source[Parser.tokenizer.position - 2] == ')':
                    #pass
                    # print("Closed parenthesis")
                #else:
                raise Exception(f"Expected ')' but got {Parser.tokenizer.next.value}, {Parser.tokenizer.next.type}")
            
            Parser.open_par = False
            Parser.tokenizer.selectNext()
        
        else:
            raise Exception(f"Expected INT, or unary, but got {Parser.tokenizer.next.type} type")
        
        return res

    def run(code):
        Parser.tokenizer = Tokenizer(prePro(code))
        Parser.tokenizer.selectNext()
        res = Parser.parseExpression()
        print(res)
        return res
    
Parser.run(source)
