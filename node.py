from symbolTable import SymbolTable


class Node:
    value = None
    children = []

    def __init__(self, value, children = None):
        # Children = None para o IntVal que só tem 1 nó filho
        self.value = value
        self.children = children
    
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self):
        if self.value == 'PLUS':
            #print(f"On BinOp: value = {self.value}; children = {self.children}")
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = a.Evaluate() + b.Evaluate()
            return res

        if self.value == 'MINUS':
            #print(f"On BinOp: value = {self.value}; children = {self.children}")
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res =  a.Evaluate() - b.Evaluate()
            return res

        if self.value == 'MULT':
            #print(f"On BinOp: value = {self.value}; children = {self.children}")
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res = a.Evaluate() * b.Evaluate()
            return res

        if self.value == 'DIV':
            #print(f"On BinOp: value = {self.value}; children = {self.children}")
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res = a.Evaluate() // b.Evaluate()
            return res

class UnOp(Node):
    def Evaluate(self):
        if self.value == 'MINUS':
            #print(f"On UnOp: value = {self.value}; children = {self.children}")
            a = self.children[0]
            # Recursion
            return -a.Evaluate()
        if self.value == 'PLUS':
            #print(f"On UnOp: value = {self.value}; children = {self.children}")
            a = self.children[0]
            # Recursion
            return a.Evaluate()
    
class Assignment(Node):
    def Evaluate(self):
        if self.value == 'ASSIGNMENT':
            identifier = self.children[0]
            expression = self.children[1]
            print("Inside Assignment")
            SymbolTable.setValue(identifier, expression.Evaluate())
            SymbolTable.getTable()
            print("Inside assignment node")

class Identifier(Node):
    def Evaluate(self):
        if id not in SymbolTable.table:
            raise Exception("Symbol not recognizes")
        return SymbolTable.getValue(self.value)

class Print(Node):
    def Evaluate(self):
        if self.value == 'PRINT':
            a = self.children[0]
            print(f"Print: {a.Evaluate()}")

class IntVal(Node):
    def Evaluate(self):
        #print(f"On IntVal: value = {self.value}; children = {self.children}")
        return self.value

class NoOp(Node):
    def Evaluate(self):
        #print(f"On NoOp: value = {self.value}; children = {self.children}")
        pass
    
class Block(Node):
    def Evaluate(self):
        print(f"Children: {self.children} -> {len(self.children)}")
        print(SymbolTable.getTable())
        for child in self.children:
            # Evaluates chlidren in order
            if child != None:
                print(f"Evaluate: {child.Evaluate()}")
            else:
                print("Child is None")