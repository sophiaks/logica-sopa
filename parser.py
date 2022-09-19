from tokenizer import Tokenizer
import re
from node import BinOp, UnOp, NoOp, IntVal, Node

def prePro(source):
    clean_code = re.sub("\s*(\W)\s*",r"\1", source)
    no_comments_hashtag = re.sub('#.*', '', clean_code)
    no_comments = re.sub('//.*', '', no_comments_hashtag).strip()
    #print(f"No comments: {no_comments}")
    if no_comments != re.sub("\s*", '', no_comments):
        raise Exception("Between two numbers there must be an operand")
    if len(no_comments) == 0:
        raise Exception("Empty input")
    return no_comments

class Parser:
    tokenizer = None
    res = 0
    open_par = False

    @staticmethod
    def parseExpression():
        #print(f"Inside parseExpression: {Parser.tokenizer.next.value}")
        res = Parser.parseTerm()
        #print(f"res from parseTerm is {res.value, res.children}")
        #print(f"Next: {Parser.tokenizer.next.value}")

        while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:
            if Parser.tokenizer.next.type == 'PLUS':
                #print("Inside ParseExpression: PLUS")
                Parser.tokenizer.selectNext()
                # BinOp(Operation, children [res, function])
                res = BinOp('PLUS', [res, Parser.parseTerm()])
                #print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")
                if Parser.tokenizer.next.value == ')' and Parser.open_par is False:
                    raise Exception("Closed par without opening")

            elif Parser.tokenizer.next.type == 'MINUS':
                Parser.tokenizer.selectNext()
                res = BinOp('MINUS', [res, Parser.parseTerm()])
                #print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

        return res
        
    @staticmethod
    def parseTerm():
        #print(f"Inside parseTerm: {Parser.tokenizer.next.value}")
        res = Parser.parseFactor()

        while Parser.tokenizer.next.type in ['MULT', 'DIV']:
            if Parser.tokenizer.next.type == 'MULT':
                Parser.tokenizer.selectNext()
                res = BinOp('MULT', [res, Parser.parseFactor()])
                #print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

            if Parser.tokenizer.next.type == 'DIV':
                Parser.tokenizer.selectNext()
                res = BinOp('DIV', [res, Parser.parseFactor()])
                #print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

        return res

    @staticmethod
    def parseFactor():
        #print(f"Inside parseFactor: {Parser.tokenizer.next.value}")
        if Parser.tokenizer.next.type == 'INT':
            res = IntVal(Parser.tokenizer.next.value)
            #print(f"!!! IntVal returned {res.value}")
            Parser.tokenizer.selectNext()
            #print(f"Next: {Parser.tokenizer.next.value}, pos = {Parser.tokenizer.position}")

        elif Parser.tokenizer.next.type == 'MINUS':
            Parser.tokenizer.selectNext()
            res = UnOp('MINUS', [Parser.parseFactor()])
            #print(f"UnOp -> MINUS: RES = {res}")

        elif Parser.tokenizer.next.type == 'PLUS':
            #print(f"Inside plus UnOP: {Parser.tokenizer.next.value}")
            Parser.tokenizer.selectNext()
            res = UnOp('PLUS', [Parser.parseFactor()])
            #print(f"UnOp -> PLUS: RES = {res}")

        elif Parser.tokenizer.next.type == 'OPEN_PAR':
            Parser.open_par = True
            Parser.tokenizer.selectNext()
            res = Parser.parseExpression()

            if Parser.tokenizer.next.type != 'CLOSE_PAR':                
                raise Exception(f"Expected ')' but got {Parser.tokenizer.next.value}, {Parser.tokenizer.next.type}")
            
            Parser.open_par = False
            Parser.tokenizer.selectNext()
        
        else:
            raise Exception(f"Expected INT, or unary, but got {Parser.tokenizer.next.type} type")
        #print(f"Returning {res.value} on parseFactor")
        return res

    def run(code):
        Parser.tokenizer = Tokenizer(prePro(code))
        Parser.tokenizer.selectNext()
        res = Parser.parseExpression()
        return res