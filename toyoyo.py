from tools.interpreter import Interpreter
import platform
import math
import os

toyoyo = Interpreter(debug=True)

@toyoyo.command()
def yell(self, *tokens):  
    if len(tokens) == 0:
        value = ""
    
    elif tokens[0].type == "COMMAND":
        value = self.raw_exec(*tokens)
    elif len(tokens) > 1:
        value = self.eval(*tokens)
    elif tokens[0].type == "VARIABLE":
        value = self.getvar(tokens[0].value)
    elif tokens[0].type == "INITVAR":
        self.error("NameError", f"'{tokens[0].value}' is not defined")
    else:
        value = tokens[0].value

    print(value)
    
@toyoyo.command(name="input")
def tyy_input(self, t=None):
    if not t:
        value = ""

    elif t.type == "STRING":
        value = t.value
    elif t.type == "VARIABLE":
        value = self.getvar(t.value)
    
    return input(value)

@toyoyo.command() 
def convert(self, original, to):
    if original.type == "VARIABLE":
        value = self.getvar(original.value)
    else:
        value = original.value
    
    if to.type != "STRING":
        self.error("ConversionError", "invalid type specified")
    
    if to.value == "int":
        return int(value)
    elif to.value == "str":
        return str(value)
    elif to.value == "float":
        return float(value)
    elif to.value == "bool":
        return bool(value)

@toyoyo.command(name="round")
def tyy_round(self, numbert, decimalt=None):
    if not decimalt:
        decimal = 0
    elif decimalt.type == "INTEGER":
        decimal = decimalt.value
    else:
        self.error("WrongTypeError", "'decimal' argument must be int")
    
    if numbert.type == "FLOAT":
        number = numbert.value
    else:
        self.error("WrongTypeError", "'number' argument must be float")
    
    if decimal == 0:
        return round(number)
    else:
        return round(number, decimal)

@toyoyo.command()
def clear(self):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

@toyoyo.command(name="if")
def tyy_if(self, *statement):
    if self.eval(*statement):
        self.__ifstate__ = 1
    else:
        self.__ifstate__ = 0

@toyoyo.command(name="elseif")
def tyy_elseif(self, *statement):
    print(self.__ifstate__)
    if self.eval(*statement) and self.__ifstate__ == 0:
        self.__ifstate__ = 1
    elif self.__ifstate__ in (0, 1):
        self.__ifstate__ = 0
    else:
        self.error("SyntaxError", "wrong syntax")

@toyoyo.command(name="else")
def tyy_else(self):
    #print(self.__ifstate__)
    if self.__ifstate__ == 1:
        self.__ifstate__ = 0
    elif self.__ifstate__ == 0:
        self.__ifstate__ = 1
    else:
        self.error("SyntaxError", "wrong syntax")

@toyoyo.command()
def end(self):
    if self.__ifstate__ in (0, 1):
        self.__ifstate__ = 2
    else:
        self.error("SyntaxError", "wrong syntax")

@toyoyo.on_execute()
def on_execute(self, *tokens):
    if not self.__ifstate__:
        return

    if len(tokens) <= 2:
        if tokens[0].type == "INITVAR":
            self.error("SyntaxError", "wrong syntax")
        else:
            return

    if tokens[0].type in ("INITVAR", "VARIABLE"):  
        if tokens[1].value == ":=" and tokens[1].type == "OPERATOR":
            if tokens[2].type == "COMMAND":
                value = self.raw_exec(*tokens[2:])
            elif len(tokens) != 3:
                value = self.eval(*tokens[2:])
            elif tokens[2].type == "INITVAR":
                self.error("NameError", f"'{tokens[2].value}' is not defined")
            else:
                value = tokens[2].value

            self.putvar(tokens[0].value, value)
          
if __name__ == "__main__":
    with open("script.tyy", "r") as f:
        toyoyo.execute_many(f.read())