from symtable import Symbol
from xml.dom.minidom import Identified
from symbolTable import SymbolTable
from tokenizer import Tokenizer
from node import BinOp, UnOp, NoOp, IntVal, Assignment, Print, Block, Identifier

reserved_words = ['if', 'else', 'Print', 'function']

# todo parser retorna um no
# chamada de block coloca como filho no block!!

# TODO:
#1: mudar parseFactor()
#2: impoementar o parseBlock
#3: ikmplementar parseStatement
#4: Trocar o run (comeca no parseBLock)

# Evaluate do block -> execute na ordem correta
# para cada filho em children -> evaluate
# filho do block não dá return

# print -> nó do print
# evaluate do filho 0 e dá print no filho 0

# = -> nó do tipo assignment -> esquerdo o identifier e direito expression
#identifier = filho 0
#= - filho 1 
#expression filho 2

# assignment nao da evaluate no filho zero - so no da direita
# valor do filho 0 recebe 3 (valor do filho 1) na symbol table -> x = 3

# qnd passa no parseFActor no identifier - retorna um nó identifier!

# x = 3 -> evaluate do 3 e tasca na symbol table
# y = x + 3 -> evaluate do x -> get da symbolTable

class Parser:
    tokenizer = None
    res = 0
    open_par = False

    @staticmethod
    def parseBlock():
        #print("Inside parseBlock")
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()

            block = Block(None, [])

            while Parser.tokenizer.next.type != 'CLOSE_BRAC':
               
                res = Parser.parseStatement()
                if res != None:
                    block.children.append(res)
                
                if Parser.tokenizer.next.type == 'EOF':
                    raise Exception("Closing brackets not found")


            if Parser.tokenizer.next.type != 'CLOSE_BRAC':
                # print(Parser.tokenizer.next.type)
                raise Exception("Closing brackets not found")

        #~~~ Consumes token ~~~#
        Parser.tokenizer.selectNext()

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

                res = Assignment('ASSIGNMENT', [id, Parser.parseExpression()])

                if Parser.tokenizer.next.type != "SEMICOLON":
                    raise Exception("Missing ;")
                    
                return res

            else:
                raise Exception(f"Invalid assignment for variable '{id.value}'")

        elif Parser.tokenizer.next.type == "SEMICOLON":
            Parser.tokenizer.selectNext()
            
        elif Parser.tokenizer.next.type == 'PRINT':
            #print("Found PRINT")
            #~~~ Consumes token ~~~#
            Parser.tokenizer.selectNext()
            
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                #~~~ Consumes token ~~~#
                Parser.tokenizer.selectNext()

                res = Print('Print', [Parser.parseExpression()])
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
            
        if Parser.tokenizer.next.type == 'SEMICOLON':
            NoOp(Parser.tokenizer.next.value)
            return
        

    @staticmethod
    def parseExpression():
        #print(f"Inside parseExpression: {Parser.tokenizer.next.value}")
        res = Parser.parseTerm()
        #print(f"res from parseTerm is {res.value, res.children}")
        #print(f"Next: {Parser.tokenizer.next.value}")

        while Parser.tokenizer.next.type in ['MINUS', 'PLUS']:

            if Parser.tokenizer.next.type == 'PLUS':
                Parser.tokenizer.selectNext()
                res = BinOp('PLUS', [res, Parser.parseTerm()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")


            elif Parser.tokenizer.next.type == 'MINUS':
                Parser.tokenizer.selectNext()
                res = BinOp('MINUS', [res, Parser.parseTerm()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

        return res
        
    @staticmethod
    def parseTerm():
        # print(f"Inside parseTerm: {Parser.tokenizer.next.value}")
        res = Parser.parseFactor()

        while Parser.tokenizer.next.type in ['MULT', 'DIV']:
            if Parser.tokenizer.next.type == 'MULT':
                Parser.tokenizer.selectNext()
                res = BinOp('MULT', [res, Parser.parseFactor()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

            if Parser.tokenizer.next.type == 'DIV':
                Parser.tokenizer.selectNext()
                res = BinOp('DIV', [res, Parser.parseFactor()])
                # print(f"BinOp returned ({res.value}, [{res.children[0].value, res.children[1].value}])")

        return res

    @staticmethod
    def parseFactor():
        #print(f"Inside parseFactor: {Parser.tokenizer.next.value}")
        if Parser.tokenizer.next.type == 'INT':
            res = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            
            #print(f"Next: {Parser.tokenizer.next.value}, pos = {Parser.tokenizer.position}")

        elif Parser.tokenizer.next.type == 'MINUS':
            Parser.tokenizer.selectNext()
            res = UnOp('MINUS', [Parser.parseFactor()])
            # print(f"UnOp -> MINUS: RES = {res.children[0].value}")

        elif Parser.tokenizer.next.type == 'PLUS':
            #print(f"Inside plus UnOP: {Parser.tokenizer.next.value}")
            Parser.tokenizer.selectNext()
            res = UnOp('PLUS', [Parser.parseFactor()])
            # print(f"UnOp -> PLUS: RES = {res.value}")

        elif Parser.tokenizer.next.type == 'IDENTIFIER':
            res = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == 'OPEN_PAR':
            Parser.open_par = True
            Parser.tokenizer.selectNext()
            res = Parser.parseExpression()

            if Parser.tokenizer.next.type != 'CLOSE_PAR':                
                raise Exception(f"Expected ')' but got {Parser.tokenizer.next.value}, {Parser.tokenizer.next.type}")
            
            Parser.open_par = False
            Parser.tokenizer.selectNext()
        
        else:
            raise Exception(f"Expected INT, or unary, but got {Parser.tokenizer.next.type} type, with {Parser.tokenizer.next.value} value")
        #print(f"Returning {res.value} on parseFactor")
        return res

    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        res = Parser.parseBlock()
        return res            
