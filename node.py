from symbolTable import SymbolTable
from funcTable import FuncTable
from aux import mprint

class Node:
    value = None
    children = []

    def __init__(self, value, children = None):
        self.value = value
        self.children = children
    
    def Evaluate(self):
        pass

class BinOp(Node):

    def Evaluate(self, ST):

      

        # Getting NODES types and values 
        # Do not confuse with Operation value of nodes :)

        a, b = self.children
        (type_a, value_a) = a.Evaluate()
        (type_b, value_b) = b.Evaluate()

        if self.value == 'PLUS':
            # Recursion
            res = int(value_a + value_b)
            plus = ('I32', res)
            return plus

        if self.value == 'EQUAL':
            res = int(value_a == value_b)
            eq = ('I32', res)
            return eq # int

        if self.value == 'GREATER_THAN':         
            res = int(value_a > value_b)
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'LESS_THAN':     
            res = int(value_a < value_b)
            tuple = ('I32', res)
            return tuple # int
        
        if self.value == 'AND':  
            res = int(value_a and value_b)
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'OR':  
            res = int(value_a or value_b)
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'MINUS':
            res =  int(value_a - value_b)
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'MULT':
            res = int(value_a * value_b)
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'DIV':
            res = int(value_a // value_b)
            tuple = ('I32', res)
            return tuple # int

        if self.value == 'CONCAT':
            res = str(value_a) + str(value_b)
            return ('STRING', res)
            
class UnOp(Node):
    def Evaluate(self, ST):

        
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
    def Evaluate(self, ST):
        var_type = self.value
        for identifier in self.children:
            ST.dec_var(var_type, identifier)

class Assignment(Node):
    def Evaluate(self, ST):
        if self.value == 'ASSIGNMENT':
            identifier_node, expression = self.children
            # Checking if identifier has been declared
            id_exists = ST.getValue(identifier_node.value)
            ST.setValue(identifier_node.value, expression.Evaluate(ST))

class Print(Node):
    def Evaluate(self, ST):
        (_type, a) = self.children[0].Evaluate()
        if _type == 'I32':
            print(int(a))
        else:
            print(a)

class If(Node):
    def Evaluate(self, ST):


        if len(self.children) == 3:
            condition = self.children[0]
            condition_true = self.children[1]
            condition_false = self.children[2]
            (_type, cond_true) = condition.Evaluate()
            if (cond_true):
                return condition_true.Evaluate()
            else:
                return condition_false.Evaluate()
        if len(self.children) == 2:
            condition = self.children[0]
            condition_true = self.children[1]
            (_type, cond_true) = condition.Evaluate()
            if (cond_true):
                return condition_true.Evaluate()

class While(Node):
    def Evaluate(self, ST):
        a, b = self.children
        (res_type, res) = a.Evaluate()
        while (res):
            b.Evaluate()
            (res_type, res) = a.Evaluate()

class Read(Node):
    def Evaluate(self, ST):
        return ('I32', int(input()))

class Identifier(Node):
    def Evaluate(self, ST):
        return ST.getValue(self.value)

class IntVal(Node):
    def Evaluate(self, ST):
        return ('I32', self.value)

class String(Node):
    def Evaluate(self, ST):
        return ('STRING', self.value)

class NoOp(Node):
    def Evaluate(self, ST):
        pass

class Return(Node):
    def Evaluate(self, ST):
        return self.children[0].Evaluate(ST)

class FuncCall(Node):
    def Evaluate(self, ST):

        mprint('_____ FUNCTION CALL (NODE) ____')
        identifier = self.value
        # Declared will be of FuncDec type
        declared = FuncTable.getFunc(identifier)
        
        localSt = SymbolTable()

        if identifier == "Main":
            mprint(f'Main block: {declared.children[-1]}')
            block = declared.children[-1]
            #  Declare and Attribute the arguments
            block.Evaluate(localSt)

        else:
            call_id = declared.children[0]
            declared_args = declared.children[1:len(declared.children)-1]
            func_block = declared.children[-1]

            attr_args = self.children

            if (len(self.children) != len(declared.children) - 2):
                raise Exception(f"Expected {len(declared.children) - 2} arguments on {identifier}, but got {len(self.children)}")
        

            mprint(f'Function children: {declared.children}')
            mprint(f'Function id: {call_id}')
            mprint(f'Function declared args: {declared_args}')
            mprint(f'Function declared args (names): {declared_args[0].children}')
            mprint(f'Function Block: {func_block}')

            mprint(f"Attributed arguments in Function Call: {attr_args}")

            for var_dec, var_attr in zip(declared_args, attr_args):
                var_dec.Evaluate(localSt)
                mprint(f'Declared argument: {var_dec.children}')
                mprint(f'Attributed value: {var_attr.value}')

class FuncDec(Node):
    def Evaluate(self, ST):

        # self.value -> function tuple (ret_type, name)
        # self.children -> function arguments (type, name) + function block

        (fn_ret_type, fn_name) = self.value
        block = self.children[-1]
        args = self.children[0:-1]
        ST.decFunc(fn_ret_type, fn_name, self)
        ST.getTable()

        return

class Block(Node):
    def Evaluate(self, ST):

        for child in self.children:
            # Evaluates chlidren in order
            res = child.Evaluate(ST)
            if res != None:
                return res
        