import shlex
import re

# regex compiled patterns
variable = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
string = re.compile(r'\".*?\"')
integer = re.compile(r'\d+')

operators = ["+", "-", "*", "/", ":="]

class Token:
    def __init__(self, value, type: str):
        self.value = value
        self.type = type
        
def tokenize(line, commands, variables):
    splitted = shlex.split(line, posix=False)
    tokens = []
    
    if line.startswith("//"):
        return

    for value in splitted:
        if integer.match(value):
            tokens.append(Token(int(value), "INTEGER"))
        elif string.match(value):
            tokens.append(Token(value[1:-1], "STRING"))
        elif value.upper() in commands:
            tokens.append(Token(value.upper(), "COMMAND"))
        elif value in operators:
            tokens.append(Token(value, "OPERATOR"))
        elif variable.match(value):
            if value in variables:
                tokens.append(Token(value, "VARIABLE"))
            else:
                tokens.append(Token(value, "INITVAR"))
        
    return tokens
                
        