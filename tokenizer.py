import re
variable_pattern = "^[A-Za-z]+[A-Za-z0-9_]*$"

reserved_wrds = {
    'Print': 'PRINT',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'Read': 'READ'
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
                temp_next += self.source[self.position]
                # concatenates number
                self.position += 1
                # If reached end of file
                if self.position >= len(self.source):
                    break
                        
            if temp_next.isdigit():
                # print(f'Found INT ({temp_next})')
                self.next = Token('INT', int(temp_next))

            elif temp_next in reserved_wrds:
                self.next = Token(reserved_wrds[temp_next], temp_next)
            
            elif bool(re.search(variable_pattern, temp_next)):
                self.next = Token('IDENTIFIER', temp_next)
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
            # print("Found OR")
            self.position += 1
            if self.source[self.position] == '|':
                 self.next = Token('OR', '||')
            else:
                raise Exception("Token not recognized: |")
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
            # print("Found SEMICOLON")
            self.position += 1
            return self.next   

        elif self.source[self.position] == "=":
            self.next = Token('ASSIGNMENT', "=")
            # print("Found EQUAL")
            self.position += 1
            if self.source[self.position] == "=":
                self.next = Token('EQUAL', "==")
                self.position += 1
            return self.next 

       

        else:
            raise Exception("Unrecognized token")

    