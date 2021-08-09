from tools.interpreter import CommandList
import math

cmdlist = CommandList()

@cmdlist.command()
def pi(self):
    return math.pi

def setup(interpreter):
    interpreter.add_cmdlist(cmdlist)