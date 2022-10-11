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
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = a.Evaluate() + b.Evaluate()
            return res

        if self.value == 'EQUAL':
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = (a.Evaluate() == b.Evaluate())
            return res

        if self.value == 'GREATER_THAN':
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = a.Evaluate() > b.Evaluate()
            return res

        if self.value == 'LESS_THAN':
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = a.Evaluate() < b.Evaluate()
            return res
        
        if self.value == 'AND':
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = a.Evaluate() and b.Evaluate()
            return res

        if self.value == 'OR':
            a = self.children[0]
            b = self.children[1]            
            # Recursion
            res = a.Evaluate() or b.Evaluate()
            return res

        if self.value == 'MINUS':
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res =  a.Evaluate() - b.Evaluate()
            return res

        if self.value == 'MULT':
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res = a.Evaluate() * b.Evaluate()
            return res

        if self.value == 'DIV':
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res = a.Evaluate() // b.Evaluate()
            return res

class UnOp(Node):
    def Evaluate(self):
        if self.value == 'MINUS':
            a = self.children[0]
            # Recursion
            return -a.Evaluate()
        if self.value == 'PLUS':
            a = self.children[0]
            # Recursion
            return a.Evaluate()
        if self.value == 'NOT':
            a = self.children[0]
            # Recursion
            return not(a.Evaluate())
    
class Assignment(Node):
    def Evaluate(self):
        if self.value == 'ASSIGNMENT':
            identifier = self.children[0]
            expression = self.children[1]
            SymbolTable.setValue(identifier, expression.Evaluate())

class Identifier(Node):
    def Evaluate(self):
        return SymbolTable.getValue(self.value)

class Print(Node):
    def Evaluate(self):
        a = self.children[0]
        print(a.Evaluate())

class If(Node):
    def Evaluate(self):
        a = self.children[0]
        b = self.children[1]
        if (a.Evaluate()):
            return b.Evaluate()
        else:
            if (len(self.children) == 3):
                c = self.children[2]
                return c.Evaluate()
            else:
                pass

class While(Node):
    def Evaluate(self):
        a = self.children[0]
        b = self.children[1]
        while (a.Evaluate()):
            b.Evaluate()

class Read(Node):
    def Evaluate(self):
        return int(input())

class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass
    
class Block(Node):
    def Evaluate(self):
        for child in self.children:
            # Evaluates chlidren in order
            child.Evaluate()
            