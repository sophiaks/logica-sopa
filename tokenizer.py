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

        if (self.source[self.position]).isdigit():
            temp_next = ''
            while (self.source[self.position]).isdigit():
                temp_next += self.source[self.position]
                # concatenates number
                self.position += 1
                # If reached end of file
                if self.position >= len(self.source):
                    break
            self.next = Token('INT', int(temp_next))
            return
            

        if self.source[self.position] == ")":
            self.next = Token('CLOSE_PAR', ")")
            self.position += 1
            return self.next   
                
        elif self.source[self.position] == '+':
            self.next = Token('PLUS', '+')
            self.position += 1
            return self.next

        elif self.source[self.position] == '-':
            self.next = Token('MINUS', '-')
            self.position += 1
            return self.next

        elif self.source[self.position] == '*':
            self.next = Token('MULT', '*')
            self.position += 1
            return self.next
         
        elif self.source[self.position] == '/':
            self.next = Token('DIV', '/')
            self.position += 1
            return self.next

        elif self.source[self.position] == '(':
            self.next = Token('OPEN_PAR', '(')
            self.position += 1
            return self.next
