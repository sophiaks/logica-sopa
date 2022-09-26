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
        if self.value == 'IDENTIFIER':
            identifier = self.children[0]
            expression = self.children[1]
            # Parser.symbol_table.set(identifier, expression)
            # print(Parser.symbol_table.table)
            return expression.Evaluate()

class Print(Node):
    def Evaluate(self):
        if self.value == 'Print':
            a = self.children[0]
            print(f"Print: {a}")
            return a.Evaluate()

class IntVal(Node):
    def Evaluate(self):
        #print(f"On IntVal: value = {self.value}; children = {self.children}")
        return self.value

class NoOp(Node):
    def Evaluate(self):
        #print(f"On NoOp: value = {self.value}; children = {self.children}")
        pass
    