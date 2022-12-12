from symbolTable import SymbolTable
from aux import mprint
from asm import ASM as asm_write


# TODO: Modificar o Evaluate() para gerar código para as seguintes operações:
# – Declaração de variáveis OK
# – Operações aritméticas OK
# – Atribuição OK
# – Condicional OK
# – Loop OK
# – Print OK

class Node:
    value = None
    children = []
    id = 0

    def __init__(self, value, children = None):
        self.value = value
        self.children = children
        self.var_counter = -4

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

        (type_a, value_a, _pos) = a.Evaluate()
        asm_write.write_line("PUSH EBX")
        (type_b, value_b, _pos) = b.Evaluate()
        asm_write.write_line("POP EAX")
        #asm_write.write_line(f'MOV EBX, {value_a} ; Evaluate() do filho IntVal da esquerda')
        #asm_write.write_line('PUSH EBX ; O BinOp guarda o resultado na pilha')
        
        #asm_write.write_line(f'MOV EBX, {value_b} ; Evaluate() do filho IntVal da direita')        
        #asm_write.write_line('POP EAX ; O BinOp recupera o valor da pilha em EAX')

        if self.value == 'PLUS':
            asm_write.write_line("ADD EAX, EBX;")
            asm_write.write_line("MOV EBX, EAX;")
            res = int(value_a + value_b)
            plus = ('I32', res, None)
            return plus

        if self.value == 'EQUAL':
            res = int(value_a == value_b)
            eq = ('I32', res, None)
            asm_write.write_line('CMP EAX, EBX')
            asm_write.write_line('CALL binop_je')
            return eq

        if self.value == 'GREATER_THAN':
            res = int(value_a > value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line('CMP EAX, EBX')
            asm_write.write_line('CALL binop_jg')
            return _tuple

        if self.value == 'LESS_THAN':
            res = int(value_a < value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line('CMP EAX, EBX')
            asm_write.write_line('CALL binop_jl')
            return _tuple
        
        if self.value == 'AND':
            res = int(value_a and value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line("AND EAX, EBX;")
            asm_write.write_line("MOV EBX, EAX;")
            return _tuple

        if self.value == 'OR':  
            res = int(value_a or value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line("OR EAX, EBX;")
            asm_write.write_line("MOV EBX, EAX;")
            return _tuple

        if self.value == 'MINUS':
            res =  int(value_a - value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line("SUB EAX, EBX;")
            asm_write.write_line("MOV EBX, EAX;")
            return _tuple

        if self.value == 'MULT':
            res = int(value_a * value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line("IMUL EAX, EBX;")
            asm_write.write_line("MOV EBX, EAX;")
            return _tuple

        if self.value == 'DIV':
            res = int(value_a // value_b)
            _tuple = ('I32', res, None)
            asm_write.write_line("IDIV EAX, EBX;")
            asm_write.write_line("MOV EBX, EAX;")
            return _tuple

        if self.value == 'CONCAT':
            res = str(value_a) + str(value_b)
            return ('STRING', res, None)
            
class UnOp(Node):
    def Evaluate(self):
        a = self.children[0]
        (type_a, value_a, _pos) = a.Evaluate()

        if type_a != 'I32':
            raise Exception("Wrong data type for unary operation")

        if self.value == 'MINUS':
            return (type_a, -value_a, None)

        if self.value == 'PLUS':
            return (type_a, value_a, None)

        if self.value == 'NOT':
            return (type_a, not(value_a), None)

class VarDec(Node):
    def Evaluate(self):
        var_type = self.value
        for identifier in self.children:
            asm_write.write_line("PUSH DWORD 0 ; alocação na primeira atribuição")
            SymbolTable.dec_var(var_type, identifier)

class Assignment(Node):
    def Evaluate(self):
        if self.value == 'ASSIGNMENT':
            identifier_node, expression = self.children

            # Checking if identifier has been declared
            (_type, _value, _pos) = SymbolTable.getValue(identifier_node.value)
            SymbolTable.setValue(identifier_node.value, expression.Evaluate())

            asm_write.write_line(f'MOV [EBP-{_pos}], EBX; resultado da atribuição')


class Print(Node):
    def Evaluate(self):
        (_type, a, _pos) = self.children[0].Evaluate()
        # if _type == 'I32':
        #     print(int(a))
        # else:
        #     print(a)
        #asm_write.write_line(f'MOV EBX, [EBP-{_pos}]')
        asm_write.write_line("PUSH EBX")
        asm_write.write_line("CALL print")
        asm_write.write_line("POP EBX")

class If(Node):
    def Evaluate(self):
        unique_id = Node.new_id()
        asm_write.write_line(f'IF_{unique_id}:')
        if len(self.children) == 3:
            condition = self.children[0]
            condition_true = self.children[1]
            condition_false = self.children[2]
            condition.Evaluate()

            asm_write.write_line('CMP EBX, False')
            asm_write.write_line(f"JE ELSE_{unique_id}")

            condition_true.Evaluate()

            asm_write.write_line(f'JMP EXIT_IF_{unique_id}')
            asm_write.write_line(f"ELSE_{unique_id}:")
       
        if len(self.children) == 3:
            # This Evaluate writes more assembly code
            (_type, eval_false, _pos) = condition_false.Evaluate()
        
        asm_write.write_line(f"EXIT_IF_{unique_id}:")

class While(Node):
    def Evaluate(self):
        mprint("Evaluating while...")
        unique_id = Node.new_id()
        asm_write.write_line(f"LOOP_{unique_id}:")
        a, b = self.children
        mprint(f"Children: {a}, {b}")

        (res_type, res, _pos) = a.Evaluate()
        asm_write.write_line("CMP EBX, False")
        asm_write.write_line(f"JE EXIT_LOOP_{unique_id}")
        
        b.Evaluate()
        asm_write.write_line(f"JMP LOOP_{unique_id}")
        asm_write.write_line(f"EXIT_LOOP_{unique_id}:")


class Read(Node):
    def Evaluate(self):
        return ('I32', int(input()), None)

class Identifier(Node):
    def Evaluate(self):
        pos = SymbolTable.getValue(self.value)[2]
        asm_write.write_line(f"MOV EBX, [EBP-{pos}]")
        return SymbolTable.getValue(self.value)

class IntVal(Node):
    def Evaluate(self):
        asm_write.write_line(f"MOV EBX, {self.value};")
        return ('I32', self.value, None)

class String(Node):
    def Evaluate(self):
        return ('STRING', self.value, None)

class NoOp(Node):
    def Evaluate(self):
        pass
    
class Block(Node):
    def Evaluate(self):
        for child in self.children:
            # Evaluates chlidren in order
            child.Evaluate()
            