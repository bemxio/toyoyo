from tools.interpreter import Interpreter

toyoyo = Interpreter(debug=False)

@toyoyo.command()
def yell(self, *tokens):  
    if len(tokens) == 0:
        value = ""
 
    elif len(tokens) > 1:
        value = self.eval(*tokens)
    elif tokens[0].type == "STRING":
        value = tokens[0].value
    elif tokens[0].type == "VARIABLE":
        value = self.getvar(tokens[0].value)

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
    
@toyoyo.on_execute()
def on_execute(self, *tokens):
    if len(tokens) == 1:
        if tokens[0].type == "INITVAR":
            self.error("SyntaxError", "wrong syntax", line, count)
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