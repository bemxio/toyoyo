from . import lexer
import sys

errtemp = """
toyoyo error; on self.__line__, {3}:
    {2}

{0}: {1}
"""

class Interpreter:
    def __init__(self, debug=False):
        self.__references__ = {}
        self.__variables__ = {}
        
        self.exec_func = None
        self.debug = debug

    def command(self, name=""):
        def wrapper(function):
            link = name or function.__name__
            self.__references__[link.upper()] = function
        
        return wrapper
    
    def on_execute(self):
        def wrapper(function):
            self.exec_func = function
        
        return wrapper
    
    def error(self, title, desc):
        print(errtemp.format(title, desc, self.__line__, self.__count__), file=sys.stderr)
        sys.exit(1)
    
    def execute(self, line):
        keys = (self.__references__.keys(), self.__variables__.keys())
        
        tokens = lexer.tokenize(self.__line__, *keys)
        if not tokens:
            return
        
        if self.exec_func:
            a = self.exec_func(self, *tokens)
            if a:
                return
        
        first, args = tokens[0], tokens[1:]
        
        if self.debug: print([(t.type, t.value) for t in tokens])
        
        if first.type == "COMMAND":
            self.__references__[first.value](self, *args)
        elif first.type == "INITVAR":
            return
        else:
            self.error("SyntaxError", "wrong syntax")

    def execute_many(self, code, splitter="\n"):
         if splitter == "\n":
             replace = ""
         else:
             replace = "\n"
         
         temp = code.replace(replace, "")
         temp = temp.split(splitter)
         
         for i, line, in enumerate(temp):
             self.__line__, self.__count__ = line, i + 1
             try:
                 self.execute(line)
             except Exception as e:
                 self.error(type(e).__name__, str(e))

    def getvar(self, name, stringify=False):
        value = self.__variables__.get(name, name)
        if type(value) == str and stringify:
            value = '"' + value + '"'
        
        return value

    def putvar(self, name, value):
        self.__variables__[name] = value
    
    def eval(self, *tokens):      
        expression = []
        for t in tokens:
            if t.type == "STRING":
                expression.append('"' + t.value + '"')
            else:
                expression.append(str(t.value))

        expression = " ".join(expression)
        try:
            return eval(expression, self.__variables__)
        except Exception as e:
            self.error(type(e).__name__, str(e))