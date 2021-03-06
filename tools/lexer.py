import shlex
import re

# regex compiled patterns
variable = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
string = re.compile(r'\".*?\"')
integer = re.compile(r'\d+')
rfloat = re.compile(r'[0-9]+\.[0-9]+')

operators = ["+", "-", "*", "/", ">", "<", ">=", "<=", "==", "!=", ":="]

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
        if rfloat.match(value):
            tokens.append(Token(float(value), "FLOAT"))
        elif integer.match(value):
            tokens.append(Token(int(value), "INTEGER"))
        elif string.match(value):
            tokens.append(Token(value[1:-1], "STRING"))
        elif value.upper() in commands:
            tokens.append(Token(value.upper(), "COMMAND"))
        elif value in operators:
            tokens.append(Token(value, "OPERATOR"))
        elif value.lower() in ("true", "false"):
            tokens.append(Token(bool(value), "BOOLEAN"))
        elif value.lower() in ("null", "none"):
            tokens.append(Token(None, "BOOLEAN"))
        elif variable.match(value):
            if value in variables:
                tokens.append(Token(value, "VARIABLE"))
            else:
                tokens.append(Token(value, "INITVAR"))
        
    return tokens
                
        