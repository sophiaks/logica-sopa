from symbolTable import SymbolTable

# TODO: Change nodes to return tuple (value, size)
# TODO Syntax: one entry for factor, one entry for 
# TODO: new node VarDec -> put type inside; if i32, node value is i32 -> children: [identifiers (number of commas)]
# var dec creates symboltable entry;
# set checks if var has been declared;
# create int = 0; string = ""
# TODO: assignment -> create two nodes - declaration or attribution -> statement has to return two nodes
# Last vardec child is assignment or some value
# If I have two variables
# Multiple variables and = -> Raise !!!

def check_type(a, b):
    if SymbolTable.getValue(a)[0] == SymbolTable.getValue(b)[0]:
        return True
    else:
        return False

class Node:
    value = None
    children = []

    def __init__(self, value, children = None):
        self.value = value
        self.children = children
    
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self):
        if self.value == 'PLUS':
            a = self.children[0]
            b = self.children[1]
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")       
            # Recursion
            res = a.Evaluate() + b.Evaluate()
            return res # int

        if self.value == 'EQUAL':
            a = self.children[0]
            b = self.children[1]
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")        
            # Recursion
            res = (a.Evaluate() == b.Evaluate())
            return res # int

        if self.value == 'GREATER_THAN':
            a = self.children[0]
            b = self.children[1]            
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res = a.Evaluate() > b.Evaluate()
            return res # int

        if self.value == 'LESS_THAN':
            a = self.children[0]
            b = self.children[1]       
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")     
            # Recursion
            res = a.Evaluate() < b.Evaluate()
            return res # int
        
        if self.value == 'AND':
            a = self.children[0]
            b = self.children[1]   
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")         
            # Recursion
            res = a.Evaluate() and b.Evaluate()
            return res # int

        if self.value == 'OR':
            a = self.children[0]
            b = self.children[1]   
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")         
            # Recursion
            res = a.Evaluate() or b.Evaluate()
            return res # int

        if self.value == 'MINUS':
            a = self.children[0]
            b = self.children[1]
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res =  a.Evaluate() - b.Evaluate()
            return res # int

        if self.value == 'MULT':
            a = self.children[0]
            b = self.children[1]
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res = a.Evaluate() * b.Evaluate()
            return res # int

        if self.value == 'DIV':
            a = self.children[0]
            b = self.children[1]
            if not check_type(a, b):
                raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res = a.Evaluate() // b.Evaluate()
            return res # int

        if self.value == 'CONCAT':
            a = self.children[0]
            b = self.children[1]
            # Recursion
            res = str(a).Evaluate() + str(b).Evaluate()
            return res #string
            
class UnOp(Node):
    def Evaluate(self):
        if self.value == 'MINUS':
            a = self.children[0]
            # Recursion
            ## TODO: check for types
            return -a.Evaluate()

        if self.value == 'PLUS':
            a = self.children[0]
            # Recursion
            ## TODO: check for types
            return a.Evaluate()

        if self.value == 'NOT':
            a = self.children[0]
            # Recursion
            ## TODO: check for types
            return not(a.Evaluate())

class VarDec(Node):
    def Evaluate(self):
        if self.value == 'DECLARATION':
            # Receives a list with identifiers and types
            for child in self.children:
                identifier = child[0]
                type = child[1]
                SymbolTable.setValue(identifier, type)
    
class Assignment(Node):
    def Evaluate(self):
        if self.value == 'ASSIGNMENT':
            identifier = self.children[0]
            # Checking if identifier has been declared
            id_exists = SymbolTable.getValue(identifier)
            expression = self.children[1]
            SymbolTable.setValue(identifier, expression.Evaluate())

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

class Identifier(Node):
    def Evaluate(self):
        return SymbolTable.getValue(self.value)

class IntVal(Node):
    def Evaluate(self):
        type = self.children[0]
        value = self.children[1]
        return (type, value)

class String(Node):
    def Evaluate(self):
        type = self.children[0]
        value = self.children[1]
        return (type, value)

class NoOp(Node):
    def Evaluate(self):
        pass
    
class Block(Node):
    def Evaluate(self):
        for child in self.children:
            # Evaluates chlidren in order
            child.Evaluate()
            