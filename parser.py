from tokenizer import Tokenizer
from node import BinOp, UnOp, NoOp, IntVal, Assignment, Print

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
class SymbolTable:
    def __init__(self):
        self.table = {}

    @staticmethod
    def getValue(value):
        return value

    @staticmethod
    def setValue(self, key, value):
        self.table[key] = value

class Parser:
    tokenizer = None
    res = 0
    open_par = False
    symbol_table = None

    @staticmethod
    def parseBlock():
        print("Inside parseBlock")
        if Parser.tokenizer.next.type == 'OPEN_BRAC':
            while Parser.tokenizer.next.type != 'CLOSE_BRAC':
                try:
                    Parser.tokenizer.selectNext()
                    res = Parser.parseStatement()
                except:
                    raise Exception("Closing brackets not found")
            print("Exiting parseBlock")

    @staticmethod
    def parseStatement():
        print("Inside parseStatement")
        if Parser.tokenizer.next.type == 'IDENTIFIER':
            id = Parser.tokenizer.next.value
            print(f"Identifier: {Parser.tokenizer.next.value}")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'EQUAL':
                print(f"Inside parseStatement: {Parser.tokenizer.next.value}")
                Parser.tokenizer.selectNext()
                print("Calling ASSIGNMENT node")
                Parser.symbol_table.setValue(id, Parser.parseExpression())
                res = Assignment('ASSIGNMENT', [id, Parser.parseExpression()])
                print(f"Assignment res: {res.children[0], res.children[1]}")
                print(f"Symbol table = {Parser.symbol_table.table}")
            
        if Parser.tokenizer.next.type == 'PRINT':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR': 
                res = Print('Print', [Parser.tokenizer.next.value])
                if Parser.tokenizer.next.type != 'CLOSE_PAR': 
                    raise Exception('Syntax Error (CLOSE_PAR)')
            else:
                raise Exception('Syntax Error (OPEN_PAR MISSING)')
        
        if Parser.tokenizer.next.type == 'SEMICOLON':
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
            if Parser.tokenizer.next.value in Parser.symbol_table.table.keys():
                print("Symbol table: {Parser.symbol_table.table}")
                res = IntVal(Parser.symbol_table.get(Parser.tokenizer.next.value))
            else:
                print("Identifier not in symbol_table")

        elif Parser.tokenizer.next.type == 'PRINT':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'OPEN_PAR':
                res = Print('Print', [Parser.tokenizer.next.value])
                if Parser.tokenizer.next.type != 'CLOSE_PAR':
                    raise Exception(f"Expected CLOSE_PAR type after expression, but got {Parser.tokenizer.next.type}")

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
        Parser.symbol_table = SymbolTable()
        print(Parser.symbol_table.table)
        Parser.tokenizer.selectNext()
        res = Parser.parseBlock()
        return res