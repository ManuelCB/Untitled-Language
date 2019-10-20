import interpreter
import os

code = interpreter.process("main.l")

def prnt(a):
    print(str(a[0]))

def inp(a): 
    o = 0
    for i in a:
        o += i
    return o

def mult(a):
    return a[0] * a[1]

def fil(a):
    o = open(os.path.join(os.getcwd(),*[f for f in a[0].replace("/"," ").split()]),a[1])
    if a[1] == "a" or a[1] == "w": o.write(str(a[2]))
    elif a[1] == "r": 
        t = o.read()
        o.close()
        return t
    o.close()

def do(a):
    global code
    c = interpreter.process(os.path.join(os.getcwd(),*[f for f in a[0].replace("/"," ").split()]))
    c.commands.extend(code.commands)
    c.run(c.text)

code.commands.append(["print",prnt])
code.commands.append(["sum",inp])
code.commands.append(["mult",mult])
code.commands.append(["run",do])
code.commands.append(["file",fil])






print(str(code.gotos))
print(str(code.text))

code.run(code.text)

print(str(code.variables))
