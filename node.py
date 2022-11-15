from symbolTable import SymbolTable
from aux import mprint
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

        # Getting NODES types and values 
        # Do not confuse with Operation value of nodes :)

        a, b = self.children
        (type_a, value_a) = a.Evaluate()
        (type_b, value_b) = b.Evaluate()

        if self.value == 'PLUS':
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")       
            # Recursion
            res = value_a + value_b
            plus = ('I32', res)
            return plus

        if self.value == 'EQUAL':
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")        
            # Recursion
            res = (value_a == value_b)
            eq = ('I32', res)
            return eq # int

        if self.value == 'GREATER_THAN':         
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res = value_a > value_b
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'LESS_THAN':     
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")     
            # Recursion
            res = value_a < value_b
            tuple = ('I32', res)
            return tuple # int
        
        if self.value == 'AND':  
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")         
            # Recursion
            res = value_a and value_b
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'OR':  
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")         
            # Recursion
            res = value_a or value_b
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'MINUS':
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res =  value_a - value_b
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'MULT':
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res = value_a * value_b
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'DIV':
            # if not check_type(a, b):
            #     raise Exception(f"Invalid types for {self.value} operation")
            # Recursion
            res = value_a // value_b
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'CONCAT':
            # Recursion
            res = str(value_a) + str(value_b)
            return ('STRING', res)
            
class UnOp(Node):
    def Evaluate(self):
        a = self.children[0]
        (type_a, value_a) = a.Evaluate()

        if type_a != 'I32':
            raise Exception("Wrong data type for unary operation")

        if self.value == 'MINUS':
            return (type_a, -value_a)

        if self.value == 'PLUS':
            return (type_a, value_a)

        if self.value == 'NOT':
            return (type_a, not(value_a))

class VarDec(Node):
    def Evaluate(self):
        var_type = self.value
        for identifier in self.children:
            SymbolTable.dec_var(var_type, identifier)

class Assignment(Node):
    def Evaluate(self):
        if self.value == 'ASSIGNMENT':
            identifier_node, expression = self.children
            # Checking if identifier has been declared
            id_exists = SymbolTable.getValue(identifier_node.value)
            SymbolTable.setValue(identifier_node.value, expression.Evaluate())

class Print(Node):
    def Evaluate(self):
        (_type, a) = self.children[0].Evaluate()
        print(a)

class If(Node):
    def Evaluate(self):
        if len(self.children) == 3:
            condition = self.children[0]
            condition_true = self.children[1]
            condition_false = self.children[2]
            (_type, cond_true) = condition.Evaluate()
            if (cond_true):
                return condition_true.Evaluate()
            else:
                return condition_false.Evaluate()
        # if (a.Evaluate()):
        #     return b.Evaluate()
        if len(self.children) == 2:
            condition = self.children[0]
            condition_true = self.children[1]
            (_type, cond_true) = condition.Evaluate()
            if (cond_true):
                return condition_true.Evaluate()

class While(Node):
    def Evaluate(self):
        a, b = self.children
        (res_type, res) = a.Evaluate()
        while (res):
            b.Evaluate()
            (res_type, res) = a.Evaluate()

class Read(Node):
    def Evaluate(self):
        return ('I32', int(input()))

class Identifier(Node):
    def Evaluate(self):
        return SymbolTable.getValue(self.value)

class IntVal(Node):
    def Evaluate(self):
        return ('I32', self.value)

class String(Node):
    def Evaluate(self):
        return ('STRING', self.value)

class NoOp(Node):
    def Evaluate(self):
        pass
    
class Block(Node):
    def Evaluate(self):
        for child in self.children:
            # Evaluates chlidren in order
            child.Evaluate()
            