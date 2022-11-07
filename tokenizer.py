import re
from aux import mprint
variable_pattern = "^[A-Za-z]+[A-Za-z0-9_]*$"

reserved_wrds = {
    'Print': 'PRINT',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'Read': 'READ',
    'i32': 'I32',
    'String': 'STRING',
    'var': 'VAR'
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.first = True

    def selectNext(self):
        
        if self.position == 0:
            self.first = False        

        if self.position >= len(self.source):
            self.next = Token('EOF', '')
            return self.next
        
        temp_next = ''
        

        if (self.source[self.position]).isdigit() or (self.source[self.position]).isalpha() or (self.source[self.position]) == '_':
            temp_next = ''
            while (self.source[self.position]).isdigit() or (self.source[self.position]).isalpha() or (self.source[self.position]) == '_':
                if temp_next in reserved_wrds:
                    self.next = temp_next
                    break
                temp_next += self.source[self.position]
                # concatenates number
                self.position += 1
                # If reached end of file
                if self.position >= len(self.source):
                    break
                        
            if temp_next.isdigit():
                mprint(f'Found INT ({temp_next})')
                self.next = Token('INT', int(temp_next))

            elif temp_next in reserved_wrds:
                self.next = Token(reserved_wrds[temp_next], temp_next)
                mprint(f"Found {self.next.value}")
        
            elif bool(re.search(variable_pattern, temp_next)):
                self.next = Token('IDENTIFIER', temp_next)
                mprint(f"Found identifier {self.next.value}")
            else:
                raise Exception("Invalid variable format")


        elif self.source[self.position] == '&':
            self.position += 1
            if self.source[self.position] == '&':
                self.next = Token('AND', '&&')
                self.position += 1
            # print("Found AND")
            else:
                raise Exception("Token not recognized: &")
            return self.next
        
        elif self.source[self.position] == '|':
            self.position += 1
            if self.source[self.position] == '|':
                self.next = Token('OR', '||')
                self.position += 1
            else:
                raise Exception("Token not recognized: |")
            return self.next

        elif self.source[self.position] == '.':
            self.next = Token('CONCAT', '.')
            self.position += 1
            return self.next

        elif self.source[self.position] == ':':
            self.next = Token('COLON', ':')
            self.position += 1
            return self.next

        elif self.source[self.position] == 'var':
            self.next = Token('VAR', 'var')
            self.position += 1
            return self.next

        elif self.source[self.position] == ',':
            self.next = Token('COMMA', ',')
            self.position += 1
            return self.next

        elif self.source[self.position] == '"':
            res_string = ''
            self.position += 1
            while self.source[self.position] != '"':
                res_string += self.source[self.position]
                self.position += 1
            #TODO: Leave string spaces (removing all the spaces currently) -> instead of "x: " we have "x:"
            self.next = Token('STRING', res_string)
            mprint(f"Res string: '{self.next.value}'")
            self.position += 1
            return self.next
        
        elif self.source[self.position] == 'type':
            self.next = Token('TYPE', 'type')
            self.position += 1
            return self.next

        elif self.source[self.position] == '>':
            self.next = Token('GREATER_THAN', '>')
            # print("Found NOT")
            self.position += 1
            return self.next

        elif self.source[self.position] == '<':
            self.next = Token('LESS_THAN', '<')
            # print("Found NOT")
            self.position += 1
            return self.next
        
        elif self.source[self.position] == '!':
            self.next = Token('NOT', '!')
            # print("Found NOT")
            self.position += 1
            return self.next
 

        elif self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            # print("Found PLUS")
            self.position += 1
            return self.next

        elif self.source[self.position] == '-':
            self.next = Token('MINUS', '-')
            # print("Found MINUS")
            self.position += 1
            return self.next

        elif self.source[self.position] == '*':
            self.next = Token('MULT', '*')
            # print("Found MULT")
            self.position += 1
            return self.next
         
        elif self.source[self.position] == '/':
            # print("Found DIV")
            self.next = Token('DIV', '/')
            self.position += 1
            return self.next

        elif self.source[self.position] == '(':
            self.next = Token('OPEN_PAR', '(')
            # print("Found OPEN_PAR")
            self.position += 1
            return self.next
        
        elif self.source[self.position] == ")":
            self.next = Token('CLOSE_PAR', ")")
            # print("Found CLOSE_PAR")
            self.position += 1
            return self.next   
        
        elif self.source[self.position] == "{":
            self.next = Token('OPEN_BRAC', "{")
            # print("Found OPEN_BRAC")
            self.position += 1
            return self.next
        
        elif self.source[self.position] == "}":
            self.next = Token('CLOSE_BRAC', "}")
            # print("Found CLOSE_BRAC")
            self.position += 1
            return self.next   

        elif self.source[self.position] == ";":
            self.next = Token('SEMICOLON', ";")
            mprint("Found SEMICOLON")
            self.position += 1
            return self.next   

        elif self.source[self.position] == "=":
            self.next = Token('ASSIGNMENT', "=")
            mprint("Found EQUAL")
            self.position += 1
            if self.source[self.position] == "=":
                self.next = Token('EQUAL', "==")
                self.position += 1
            return self.next 

       

        else:
            raise Exception("Unrecognized token")

    