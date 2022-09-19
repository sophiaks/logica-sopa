from contextlib import redirect_stderr

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
    

class IntVal(Node):
    def Evaluate(self):
        #print(f"On IntVal: value = {self.value}; children = {self.children}")
        return self.value

class NoOp(Node):
    def Evaluate(self):
        #print(f"On NoOp: value = {self.value}; children = {self.children}")
        pass
    