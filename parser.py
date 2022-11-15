from tokenize import String
from tokenizer import Tokenizer
from node import BinOp, UnOp, NoOp, IntVal, Assignment, Print, Block, Identifier, Read, If, VarDec, While, String
from aux import mprint
reserved_words = ['if', 'else', 'Print', 'function']

class Parser:
    tokenizer = None
    res = 0
    open_par = False

    @staticmethod
    def parseBlock():
        block = Block(None, [])
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            while Parser.tokenizer.next.type != 'CLOSE_BRAC':
                res = Parser.parseStatement()
                if res != None: # Might be useless
                    block.children.append(res)
                
                if Parser.tokenizer.next.type == 'EOF':
                    raise Exception("Closing brackets not found")
            
            #~~~ Consumes closing brackets token ~~~#
            Parser.tokenizer.selectNext()
        
        return block

    @staticmethod
    def parseStatement():

        if Parser.tokenizer.next.type == 'INT':
            raise Exception("Statements must not start with an INT type")

        ##      BLOCK       ##
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            return Parser.parseBlock()

        ##      ASSIGNMENT       ##
        if Parser.tokenizer.next.type == 'IDENTIFIER':
            mprint("ASSIGNMENT")
            mprint(f"    - Assigning value to {Parser.tokenizer.next.value}")
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

        ###     WHILE    ###
            
        elif Parser.tokenizer.next.type == "WHILE":
            mprint("WHILE CLAUSE")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                Parser.tokenizer.selectNext()
                resCondition = Parser.parseRelExpression()
                mprint("Condition Parsed")
            if Parser.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Missing )")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_BRAC':
                resStatement = Parser.parseBlock()
                mprint("Block parsed")
            else:
                resStatement = Parser.parseStatement()
                mprint("Statement parsed")
            res = While('WHILE', [resCondition, resStatement])
            return res

        ##      IF       ##

        elif Parser.tokenizer.next.type == "IF":
            mprint("IF CLAUSE")
            Parser.tokenizer.selectNext()

            # Condition is mandatory
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                Parser.tokenizer.selectNext()
                resCondition = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != 'CLOSE_PAR':
                    raise Exception("Missing )")
                # ~~~ Consumes CLOSE_PAR token ~~~ #
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type == 'OPEN_BRAC':
                # Block if clause
                    resStatement = Parser.parseBlock()
                # Empty if clause
                elif Parser.tokenizer.next.type == "ELSE":
                    raise Exception("Empty if clause")
                # One-line if clause
                else:
                    mprint("    - One-liner If")
                    resStatement = Parser.parseStatement()
                    Parser.tokenizer.selectNext()
                    mprint(f"resStatement is {resStatement}")
                
                if Parser.tokenizer.next.type == "ELSE":
                    mprint("    - Else clause")
                    Parser.tokenizer.selectNext()
                    # If-else clause
                    res = If('IF', [resCondition, resStatement, Parser.parseStatement()])

                else:
                    # No else
                    mprint("    - If with no else")
                    mprint(Parser.tokenizer.next.type)
                    res = If('IF', [resCondition, resStatement])
            
            # More than one else
            if Parser.tokenizer.next.type == "ELSE":
                raise Exception("If clause has wrong syntax")
            return res
            
        ###     VARIABLE DECLARATION     ###

        elif Parser.tokenizer.next.type == 'VAR':
            mprint("VARIABLE DECLARATION")
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == 'IDENTIFIER':
                res = VarDec("", [])
                # Adds first identifier to list
                res.children.append(Parser.tokenizer.next.value)
                mprint(f"    - Declaring {Parser.tokenizer.next.value}")
                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()

                while Parser.tokenizer.next.type == 'COMMA':
                    #~~~ Consumes token ~~~#
                    Parser.tokenizer.selectNext()
                    res.children.append(Parser.tokenizer.next.value)
                    mprint(f"    - Declaring {Parser.tokenizer.next.value}")
                    #~~~ Consumes token ~~~#
                    Parser.tokenizer.selectNext()
                
                if Parser.tokenizer.next.type == 'COLON':
                    #~~~ Consumes token ~~~#
                    Parser.tokenizer.selectNext()

                    res.value = Parser.tokenizer.next.type

                    #~~~ Consumes token ~~~#
                    Parser.tokenizer.selectNext()
                    
                    if Parser.tokenizer.next.type == 'EQUAL':
                        raise Exception("Cannot declare and assign at the same time")

                    if Parser.tokenizer.next.type != 'SEMICOLON':
                        raise Exception("Missing ';'")

                # #~~~ Consumes token ~~~#

            return res
        
        ###     PRINT   ###

        elif Parser.tokenizer.next.type == 'PRINT':
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

        while Parser.tokenizer.next.type in ['EQUAL', 'GREATER_THAN', 'LESS_THAN', 'CONCAT']:

            if Parser.tokenizer.next.type == 'GREATER_THAN':
                Parser.tokenizer.selectNext()
                res = BinOp('GREATER_THAN', [res, Parser.parseExpression()])

            elif Parser.tokenizer.next.type == 'LESS_THAN':
                Parser.tokenizer.selectNext()
                res = BinOp('LESS_THAN', [res, Parser.parseExpression()])

            elif Parser.tokenizer.next.type == 'EQUAL':
                Parser.tokenizer.selectNext()
                res = BinOp('EQUAL', [res, Parser.parseExpression()])

            elif Parser.tokenizer.next.type == 'CONCAT':
                Parser.tokenizer.selectNext()
                res = BinOp('CONCAT', [res, Parser.parseExpression()])

        return res

    @staticmethod
    def parseExpression():

        res = Parser.parseTerm()

        while Parser.tokenizer.next.type in ['MINUS', 'PLUS', 'OR']:

            if Parser.tokenizer.next.type == 'PLUS':
                Parser.tokenizer.selectNext()
                res = BinOp('PLUS', [res, Parser.parseTerm()])

            elif Parser.tokenizer.next.type == 'MINUS':
                Parser.tokenizer.selectNext()
                res = BinOp('MINUS', [res, Parser.parseTerm()])

            elif Parser.tokenizer.next.type == 'OR':
                Parser.tokenizer.selectNext()
                res = BinOp('OR', [res, Parser.parseTerm()])

        return res
        
    @staticmethod
    def parseTerm():

        res = Parser.parseFactor()

        while Parser.tokenizer.next.type in ['MULT', 'DIV', 'AND']:
            if Parser.tokenizer.next.type == 'MULT':
                Parser.tokenizer.selectNext()
                res = BinOp('MULT', [res, Parser.parseFactor()])

            if Parser.tokenizer.next.type == 'DIV':
                Parser.tokenizer.selectNext()
                res = BinOp('DIV', [res, Parser.parseFactor()])

            if Parser.tokenizer.next.type == 'AND':
                Parser.tokenizer.selectNext()
                res = BinOp('AND', [res, Parser.parseFactor()])

        return res

    @staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == 'INT':
            res = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            return res
        
        elif Parser.tokenizer.next.type == 'IDENTIFIER':
            res = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            return res

        elif Parser.tokenizer.next.type == 'STRING':
            res = String(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            return res
        ## UNARY OPERATIONS ##

        elif Parser.tokenizer.next.type == 'MINUS':
            Parser.tokenizer.selectNext()
            res = UnOp('MINUS', [Parser.parseFactor()])
            return res

        elif Parser.tokenizer.next.type == 'PLUS':
            Parser.tokenizer.selectNext()
            res = UnOp('PLUS', [Parser.parseFactor()])
            return res

        elif Parser.tokenizer.next.type == 'NOT':
            Parser.tokenizer.selectNext()
            res = UnOp('NOT', [Parser.parseFactor()])
            return res

        ## BINARY OPERATIONS ##

        elif Parser.tokenizer.next.type == 'OPEN_PAR':
            Parser.open_par = True
            Parser.tokenizer.selectNext()
            res = Parser.parseRelExpression()

            if Parser.tokenizer.next.type != 'CLOSE_PAR':                
                raise Exception(f"Expected ')' but got {Parser.tokenizer.next.value}, {Parser.tokenizer.next.type}")
            
            Parser.open_par = False
            Parser.tokenizer.selectNext()
            return res

        ## READ OPERATIONS ##

        elif Parser.tokenizer.next.type == 'READ':
            mprint("READING INPUT")
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
        return res

    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        res = Parser.parseBlock()
        return res            
