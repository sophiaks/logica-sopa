from tokenize import String
from tokenizer import Tokenizer
from node import BinOp, UnOp, NoOp, IntVal, Assignment, Print, Block, Identifier, Read, If, VarDec, While, String, FuncDec, FuncCall, Return
from aux import mprint
reserved_words = ['if', 'else', 'Print', 'function']

class Parser:
    tokenizer = None
    res = 0
    open_par = False

    @staticmethod
    def parseProgram():
        declarations = []
        while Parser.tokenizer.next.type != 'EOF':
            dec = Parser.parseDeclaration()
            declarations.append(dec)
        block = Block('BLOCK', declarations)
        return block

    @staticmethod
    def parseDeclaration():
        # Initiating declaration node without children
        dec = FuncDec(None, [])
        func_type = None
        fn_block = None
        if Parser.tokenizer.next.type == 'FUNCTION':
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'IDENTIFIER':
                raise Exception("Missing identifier on function declaration")
            func_name = Parser.tokenizer.next.value
            fn_id_node = Identifier(Parser.tokenizer.next.value)
            dec.children.append(fn_id_node)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != 'OPEN_PAR':
                raise SyntaxError("Syntax Error")
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type != 'CLOSE_PAR':
                if Parser.tokenizer.next.type == 'IDENTIFIER':
                    funct_id_local = [Parser.tokenizer.next.value]
                    Parser.tokenizer.selectNext()
                    while Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == 'IDENTIFIER':
                            funct_id_local.append(Parser.tokenizer.next.value)
                            Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != 'COLON':
                        raise Exception("Missing argument type")
                    Parser.tokenizer.selectNext()
                    type_local = Parser.tokenizer.next.value
                    vardec = VarDec(type_local, funct_id_local)
                    
                    dec.children.append(vardec)
                
                    if Parser.tokenizer.next.type not in ['STRING', 'I32']:
                        raise Exception('Function type not recognized')
                    
                    Parser.tokenizer.selectNext()
            
                if Parser.tokenizer.next.type == 'COMMA':
                    Parser.tokenizer.selectNext()

            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == 'ARROW':

                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type not in ['STRING', 'I32']:
                    raise Exception("Missing function return type")
                func_type = Parser.tokenizer.next.type
                Parser.tokenizer.selectNext()
            else: 
                if Parser.tokenizer.next.type != 'OPEN_BRAC':
                    raise Exception("Syntax Error")

            if Parser.tokenizer.next.type == 'OPEN_BRAC':
                fn_block = Parser.parseBlock()

            dec.value = (func_type, func_name)
            dec.children.append(fn_block)
            

            mprint('________________')
            mprint("\nFinal FuncDec: ")
            mprint(f"Value: {dec.value}")
            mprint(f"Args: {dec.children}")
            mprint(f"Block: {fn_block.children}")
            mprint('________________')

            return dec

    @staticmethod
    def parseBlock():

        block = Block(None, [])
        
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            while Parser.tokenizer.next.type != 'CLOSE_BRAC':
                res = Parser.parseStatement()
                
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

        ##      IF       ##
        elif Parser.tokenizer.next.type == "IF":
            #mprint("IF CLAUSE")
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
                    #mprint("    - One-liner If")
                    resStatement = Parser.parseStatement()
                    Parser.tokenizer.selectNext()
                    #mprint(f"resStatement is {resStatement}")
                
                if Parser.tokenizer.next.type == "ELSE":
                    #mprint("    - Else clause")
                    Parser.tokenizer.selectNext()
                    # If-else clause
                    res = If('IF', [resCondition, resStatement, Parser.parseStatement()])

                else:
                    # No else
                    #mprint("    - If with no else")
                    #mprint(Parser.tokenizer.next.type)
                    res = If('IF', [resCondition, resStatement])
            
            # More than one else
            if Parser.tokenizer.next.type == "ELSE":
                raise Exception("If clause has wrong syntax")
            return res
            
        ###     VARIABLE DECLARATION     ###
        elif Parser.tokenizer.next.type == 'VAR':
            #mprint("VARIABLE DECLARATION")
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == 'IDENTIFIER':
                res = VarDec("", [])
                # Adds first identifier to list
                res.children.append(Parser.tokenizer.next.value)
                #mprint(f"    - Declaring {Parser.tokenizer.next.value}")
                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()

                while Parser.tokenizer.next.type == 'COMMA':
                    #~~~ Consumes token ~~~#
                    Parser.tokenizer.selectNext()
                    res.children.append(Parser.tokenizer.next.value)
                    # mprint(f"    - Declaring {Parser.tokenizer.next.value}")
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

            return res
        
        ###     PRINT   ###
        elif Parser.tokenizer.next.type == 'PRINT':
            #mprint("CALLING PRINT")
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
        
        elif Parser.tokenizer.next.type == 'RETURN':
            res = Return('RETURN', [])
            Parser.tokenizer.selectNext()

            res.children = Parser.parseRelExpression()
            return res

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
        
        ### FUNC CALL ###
        elif Parser.tokenizer.next.type == 'IDENTIFIER':
            identifier = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                arg_list = []
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != 'CLOSE_PAR':
                    arg = Parser.parseRelExpression()
                    arg_list.append(arg)
                    if Parser.tokenizer.next.type == 'COMMA':
                        Parser.tokenizer.selectNext()
                res = FuncCall(identifier, arg_list)
                Parser.tokenizer.selectNext()
            else:
                res = Identifier(identifier)
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
            #mprint("READING INPUT")
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

    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        res = Parser.parseProgram()
        res.children.append(FuncCall("Main", []))
        return res            
