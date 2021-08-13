from tools.interpreter import CommandList
import math

allowed = [int, str, float, bool]
cmdlist = CommandList()

functions = {}
for name, function in vars(math).items():
    if callable(function) or type(function) in allowed:
        functions[f"math_{name}"] = function

def setup(interpreter):
    interpreter.add_cmdlist(cmdlist)