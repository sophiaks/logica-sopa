from symtable import Symbol
from symbolTable import SymbolTable
from tokenizer import Tokenizer
from node import BinOp, UnOp, NoOp, IntVal, Assignment, Print, Block, Identifier, Read, If, While

reserved_words = ['if', 'else', 'Print', 'function']

class Parser:
    tokenizer = None
    res = 0
    open_par = False

    @staticmethod
    def parseBlock():
        block = None
        #print("Inside parseBlock")
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == 'INT':
                raise Exception("Variable names must not start with an INT type")

            block = Block(None, [])

            while Parser.tokenizer.next.type != 'CLOSE_BRAC':
               
                res = Parser.parseStatement()
                if res != None:
                    block.children.append(res)
                
                if Parser.tokenizer.next.type == 'EOF':
                    raise Exception("Closing brackets not found")


            if Parser.tokenizer.next.type != 'CLOSE_BRAC':
                print(Parser.tokenizer.next.type)
                raise Exception("Closing brackets not found")

        #~~~ Consumes token ~~~#
        Parser.tokenizer.selectNext()
    
        if Parser.tokenizer.next.type != 'EOF':
                    raise Exception(f"Expected EOF type, but got {Parser.tokenizer.next.type}")

        return block

    @staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == 'IDENTIFIER':
            id = Identifier(Parser.tokenizer.next.value)
            
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == 'ASSIGNMENT':
                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()

                res = Assignment('ASSIGNMENT', [id, Parser.parseRelExpression()])

                if Parser.tokenizer.next.type != "SEMICOLON":
                    raise Exception("Missing ;")
                    
                return res

            else:
                raise Exception(f"Invalid assignment for variable '{id.value}'")

        elif Parser.tokenizer.next.type == "SEMICOLON":
            Parser.tokenizer.selectNext()
            res = NoOp(Parser.tokenizer.next.value)
            return res
            
        elif Parser.tokenizer.next.type == "WHILE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                Parser.tokenizer.selectNext()
                resCondition = Parser.parseRelExpression()
            if Parser.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Missing )")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_BRAC':
                resStatement = Parser.parseBlock()
            else:
                resStatement = Parser.parseStatement()
            res = While('WHILE', [resCondition, resStatement])
            return res

        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                Parser.tokenizer.selectNext()
                resCondition = Parser.parseRelExpression()
            if Parser.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Missing )")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_BRAC':
                resStatement = Parser.parseBlock()
            else:
                resStatement = Parser.parseStatement()
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                res = If('IF', [resCondition, resStatement, Parser.parseStatement()])
            else:
                res = If('IF', [resCondition, resStatement])
            if Parser.tokenizer.next.type == "ELSE":
                raise Exception("If clause has wrong sytntax")
            return res
            


        elif Parser.tokenizer.next.type == 'PRINT':
            #print("Found PRINT")
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()
            
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()

                res = Print('Print', [Parser.parseRelExpression()])
                if Parser.tokenizer.next.type != 'CLOSE_PAR':
                    raise Exception("Missing ')'")
                
                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != 'SEMICOLON':
                    raise Exception("Missing ';'")

                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()
                
                return res

            else:
                raise Exception(f'Syntax Error: Expected OPEN_PAR but got {Parser.tokenizer.next.value}')
        
        else:
            return Parser.parseBlock()

        

    @staticmethod
    def parseRelExpression():

        res = Parser.parseExpression()

        while Parser.tokenizer.next.type in ['EQUAL', 'GREATER_THAN', 'LESS_THAN']:

            if Parser.tokenizer.next.type == 'GREATER_THAN':
                Parser.tokenizer.selectNext()
                res = BinOp('GREATER_THAN', [res, Parser.parseExpression()])

            elif Parser.tokenizer.next.type == 'LESS_THAN':
                Parser.tokenizer.selectNext()
                res = BinOp('LESS_THAN', [res, Parser.parseExpression()])

            elif Parser.tokenizer.next.type == 'EQUAL':
                Parser.tokenizer.selectNext()
                res = BinOp('EQUAL', [res, Parser.parseExpression()])

        return res

    @staticmethod
    def parseExpression():
        #print(f"Inside parseExpression: {Parser.tokenizer.next.value}")
        res = Parser.parseTerm()
        #print(f"res from parseTerm is {res.value, res.children}")
        #print(f"Next: {Parser.tokenizer.next.value}")

        while Parser.tokenizer.next.type in ['MINUS', 'PLUS', 'OR']:

            if Parser.tokenizer.next.type == 'PLUS':
                Parser.tokenizer.selectNext()
                res = BinOp('PLUS', [res, Parser.parseTerm()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")


            elif Parser.tokenizer.next.type == 'MINUS':
                Parser.tokenizer.selectNext()
                res = BinOp('MINUS', [res, Parser.parseTerm()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

            elif Parser.tokenizer.next.type == 'OR':
                Parser.tokenizer.selectNext()
                res = BinOp('OR', [res, Parser.parseTerm()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")


        return res
        
    @staticmethod
    def parseTerm():
        # print(f"Inside parseTerm: {Parser.tokenizer.next.value}")
        res = Parser.parseFactor()

        while Parser.tokenizer.next.type in ['MULT', 'DIV', 'AND']:
            if Parser.tokenizer.next.type == 'MULT':
                Parser.tokenizer.selectNext()
                res = BinOp('MULT', [res, Parser.parseFactor()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

            if Parser.tokenizer.next.type == 'DIV':
                Parser.tokenizer.selectNext()
                res = BinOp('DIV', [res, Parser.parseFactor()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

            if Parser.tokenizer.next.type == 'AND':
                Parser.tokenizer.selectNext()
                res = BinOp('AND', [res, Parser.parseFactor()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")


        return res

    @staticmethod
    def parseFactor():
        #print(f"Inside parseFactor: {Parser.tokenizer.next.value}")
        if Parser.tokenizer.next.type == 'INT':
            res = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            
        ## UNARY OPERATIONS ##

        elif Parser.tokenizer.next.type == 'MINUS':
            Parser.tokenizer.selectNext()
            res = UnOp('MINUS', [Parser.parseFactor()])
            # print(f"UnOp -> MINUS: RES = {res.children[0].value}")

        elif Parser.tokenizer.next.type == 'PLUS':
            #print(f"Inside plus UnOP: {Parser.tokenizer.next.value}")
            Parser.tokenizer.selectNext()
            res = UnOp('PLUS', [Parser.parseFactor()])
            # print(f"UnOp -> PLUS: RES = {res.value}")

        elif Parser.tokenizer.next.type == 'NOT':
            #print(f"Inside plus UnOP: {Parser.tokenizer.next.value}")
            Parser.tokenizer.selectNext()
            res = UnOp('NOT', [Parser.parseFactor()])
            # print(f"UnOp -> PLUS: RES = {res.value}")

        ## BINARY OPERATIONS ##

        elif Parser.tokenizer.next.type == 'IDENTIFIER':
            res = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == 'OPEN_PAR':
            Parser.open_par = True
            Parser.tokenizer.selectNext()
            res = Parser.parseRelExpression()

            if Parser.tokenizer.next.type != 'CLOSE_PAR':                
                raise Exception(f"Expected ')' but got {Parser.tokenizer.next.value}, {Parser.tokenizer.next.type}")
            
            Parser.open_par = False
            Parser.tokenizer.selectNext()

        ## READ OPERATIONS ##
        elif Parser.tokenizer.next.type == 'READ':
            res = Read('READ')
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'OPEN_PAR':
                raise Exception("Missing (")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Missing )")
            Parser.tokenizer.selectNext()
            return res
        
        else:
            raise Exception(f"Expected INT, or unary, but got {Parser.tokenizer.next.type} type, with {Parser.tokenizer.next.value} value")
        #print(f"Returning {res.value} on parseFactor")
        return res

    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        res = Parser.parseBlock()
        return res            
