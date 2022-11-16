from symbolTable import SymbolTable
from aux import mprint
from asm import asm_clau


# TODO: Modificar o Evaluate() para gerar código para as seguintes operações:
# – Declaração de variáveis
# – Operações aritméticas
# – Atribuição
# – Condicional
# – Loop
# – Print

class Node:
    value = None
    children = []
    id = 0

    def __init__(self, value, children = None):
        self.value = value
        self.children = children

    @staticmethod
    def new_id():
        Node.id += 1
        return Node.id
    
    def Evaluate(self):
        pass

class BinOp(Node):

    def Evaluate(self):

        # Getting NODES types and values 
        # Do not confuse with Operation value of nodes :)

        a, b = self.children
        (type_a, value_a) = a.Evaluate()
        (type_b, value_b) = b.Evaluate()

        asm_clau.write_line(f'MOV EBX, {value_a} ; Evaluate() do filho IntVal da esquerda')
        asm_clau.write_line('PUSH EBX ; O BinOp guarda o resultado na pilha')
        
        asm_clau.write_line(f'MOV EBX, {value_b} ; Evaluate() do filho IntVal da direita')        
        asm_clau.write_line('POP EAX ; O BinOp recupera o valor da pilha em EAX')

        #'ADD EAX, EBX ; O BinOp executa a operação correspondente'
        #'MOV EBX, EAX ; O BinOp retorna o valor em EBX (sempre EBX)'

        if self.value == 'PLUS':
            asm_clau.write_line("ADD EAX, EBX;")
            asm_clau.write_line("MOV EBX, EAX;")
            res = int(value_a + value_b)
            # plus = ('I32', res)
            # return plus

        if self.value == 'EQUAL':
            res = int(value_a == value_b)
            eq = ('I32', res)
            asm_clau.write_line('CMP EAX, EBX')
            asm_clau.write_line('CALL binop_je')
            return eq

        if self.value == 'GREATER_THAN':
            res = int(value_a > value_b)
            tuple = ('I32', res)
            asm_clau.write_line('CMP EAX, EBX')
            asm_clau.write_line('CALL binop_jg')
            return tuple

        if self.value == 'LESS_THAN':
            res = int(value_a < value_b)
            tuple = ('I32', res)
            asm_clau.write_line('CMP EAX, EBX')
            asm_clau.write_line('CALL binop_jl')
            return tuple
        
        if self.value == 'AND':
            res = int(value_a and value_b)
            tuple = ('I32', res)
            asm_clau.write_line("AND EAX, EBX;")
            asm_clau.write_line("MOV EBX, EAX;")
            return tuple

        if self.value == 'OR':  
            res = int(value_a or value_b)
            tuple = ('I32', res)
            asm_clau.write_line("OR EAX, EBX;")
            asm_clau.write_line("MOV EBX, EAX;")
            return tuple

        if self.value == 'MINUS':
            res =  int(value_a - value_b)
            tuple = ('I32', res)
            asm_clau.write_line("SUB EAX, EBX;")
            asm_clau.write_line("MOV EBX, EAX;")
            return tuple

        if self.value == 'MULT':
            res = int(value_a * value_b)
            tuple = ('I32', res)
            asm_clau.write_line("IMUL EAX, EBX;")
            asm_clau.write_line("MOV EBX, EAX;")
            return tuple

        if self.value == 'DIV':
            res = int(value_a // value_b)
            tuple = ('I32', res)
            asm_clau.write_line("IDIV EAX, EBX;")
            asm_clau.write_line("MOV EBX, EAX;")
            return tuple

        if self.value == 'CONCAT':
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
            #asm_clau.write_line("PUSH DWORD 0 ; alocação na primeira atribuição")
            SymbolTable.dec_var(var_type, identifier)

class Assignment(Node):
    def Evaluate(self):
        if self.value == 'ASSIGNMENT':
            identifier_node, expression = self.children

            # Checking if identifier has been declared
            (_var_type, _value, pos) = SymbolTable.getValue(identifier_node.value)
            SymbolTable.setValue(identifier_node.value, expression.Evaluate())

            asm_clau.write_line(f'MOV EBX, {expression.Evaluate()} ; Evaluate() do filho da direita')
            asm_clau.write_line(f'MOV [EBP-{pos}], EBX; resultado da atribuição - não há return')


class Print(Node):
    def Evaluate(self):
        (_type, a) = self.children[0].Evaluate()
        if _type == 'I32':
            print(int(a))
        else:
            print(a)
        asm_clau.write_line("PUSH EBX")
        asm_clau.write_line("CALL print")
        asm_clau.write_line("POP EBX")

class If(Node):
    def Evaluate(self):
        unique_id = Node.new_id()
        asm_clau.write_line(f'IF_{unique_id}:')
        if len(self.children) == 3:
            condition = self.children[0]
            condition_true = self.children[1]
            condition_false = self.children[2]
            (_type, cond_true, _pos) = condition.Evaluate()

            asm_clau.write_line('CMP EBX, False')
            asm_clau.write_line(f"JE ELSE_{unique_id}")

            (_type, eval_true, _pos) = condition_true.Evaluate()

            asm_clau.write_line(f'JMP EXIT_IF_{unique_id}')
            asm_clau.write_line(f"ELSE_{unique_id}:")
       
        if len(self.children) == 3:
            # This Evaluate writes more assembly code
            (_type, eval_false, _pos) = condition_false.Evaluate()
        
        asm_clau.write_line(f"EXIT_IF_{unique_id}:")

class While(Node):
    def Evaluate(self):
        unique_id = Node.new_id()
        asm_clau.write_line(f"LOOP_{unique_id}:")
        a, b = self.children
        (res_type, res, _pos) = a.Evaluate()
        asm_clau.write("CMP EBX, False")
        asm_clau.write(f"JE EXIT_LOOP_{unique_id}")
        (res_type_b, res_b, _pos) = b.Evaluate()
        # No need for a while loop because we have JUMPS in the assembly code 
        asm_clau.write_line(f"JMP LOOP_{unique_id}")
        asm_clau.write_line(f"EXIT_LOOP_{unique_id}:")

class Read(Node):
    def Evaluate(self):
        return ('I32', int(input()))

class Identifier(Node):
    def Evaluate(self):
        return SymbolTable.getValue(self.value)

class IntVal(Node):
    def Evaluate(self):
        #asm_clau.write_line(f"MOV EBX, {self.value};")
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
            