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
        print("Inside parseBlock")
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            block = Block(None, [])
            while Parser.tokenizer.next.type != 'CLOSE_BRAC':
                try:
                    Parser.tokenizer.selectNext()
                    res = Parser.parseStatement()
                    print(f"RES: {res}")
                    if res != None:
                        block.children.append(res)
                    else:
                        print("Child is None")
                except:
                    raise Exception("Closing brackets not found")
            print("Exiting parseBlock")
        return block

    @staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == 'IDENTIFIER':
            id = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'ASSIGNMENT':
                Parser.tokenizer.selectNext()
                res = Assignment('ASSIGNMENT', [id, Parser.parseExpression()])

                # Assignment node OK -> Why is SymbolTable not updating?
                
                if Parser.tokenizer.next.type != "SEMICOLON":
                    raise Exception("Missing ;")
                return res
            if Parser.tokenizer.next.type == "SEMICOLON":
                Parser.tokenizer.selectNext()
            
        elif Parser.tokenizer.next.type == 'PRINT':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR': 
                res = Print('Print', [Parser.parseExpression()])
                return res
            else:
                raise Exception('Syntax Error (OPEN_PAR MISSING)')
        elif Parser.tokenizer.next.type == 'SEMICOLON':
            NoOp(Parser.tokenizer.next.value)


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

        elif Parser.tokenizer.next.type == 'IDENTIFIER':
            res = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()

        # elif Parser.tokenizer.next.type == 'PRINT':
        #     Parser.tokenizer.selectNext()
        #     if Parser.tokenizer.next.type == 'OPEN_PAR':
        #         res = Print('Print', [Parser.tokenizer.next.value])
        #         print("Type is PRINT: {res}")
        #         if Parser.tokenizer.next.type != 'CLOSE_PAR':
        #             raise Exception(f"Expected CLOSE_PAR type after expression, but got {Parser.tokenizer.next.type}")

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
        print(res.Evaluate())
        return res            
