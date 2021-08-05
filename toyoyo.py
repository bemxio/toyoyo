from tools.interpreter import Interpreter

toyoyo = Interpreter(debug=False)

@toyoyo.command()
def yell(self, t):
    if t.type == "STRING":
        print(t.value)
    elif t.type == "VARIABLE":
        print(self.getvar(t.value))

@toyoyo.on_execute()
def on_execute(self, *tokens):
    if len(tokens) == 1:
        if tokens[0].type == "INITVAR":
            self.error("SyntaxError", "wrong syntax", line, count)
        else:
            return

    if tokens[0].type in ("INITVAR", "VARIABLE"):  
        if tokens[1].value == ":=" and tokens[1].type == "OPERATOR":
            if len(tokens) != 3:
                value = self.eval(*tokens[2:])
            elif tokens[2].type == "INITVAR":
                self.error("NameError", f"'{tokens[2].value}' is not defined")
            else:
                value = tokens[2].value

            self.putvar(tokens[0].value, value)
          
if __name__ == "__main__":
    with open("script.tyy", "r") as f:
        toyoyo.execute_many(f.read())