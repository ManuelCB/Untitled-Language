class process(object):

    def __init__(self, file):
        n = 0
        self.commands = []
        self.variables = []
        self.functions = []
        self.gotos = []
        f = open(file,"r")
        s = f.read().splitlines()
        r = []
        for line in s: 
            l = notabs(line)
            c = self.to_command(l)
            if c != None and len(l.split()) == 1: 
                r.append(c)
                n += 1
                continue
            try:
                if l[-1] == ":":
                    self.gotos.append([l[:-1],n])
                else: 
                    r.append(l)
                    n += 1
            except IndexError: pass

        f.close()
        self.text = clean(r)

    def run(self,t):
        do = True
        number = 0
        while True:
            try:
                line = t[number]
            except IndexError: break
            if type(line) == str:
                if len(line.split()) > 1:
                    if line.split()[1] == "=": 
                        self.variables.append(self.reanalyze(line.split()))
                    if line.split()[1] == "+=":
                        n = int(self.variables[self.find_var_number(line.split()[0])][1][1:-1]) + int(self.analyze(self.reanalyze([None,None,line.split()[2]])[1]))
                        self.variables[self.find_var_number(line.split()[0])][1] = "(" + str(n) + ")"
                    if line.split()[1] == "-=":
                        n = int(self.variables[self.find_var_number(line.split()[0])][1][1:-1]) - int(self.analyze(self.reanalyze([None,None,line.split()[2]])[1]))
                        self.variables[self.find_var_number(line.split()[0])][1] = "(" + str(n) + ")"
                    if line.split()[1] == "==":
                        self.variables[self.find_var_number(line.split()[0])][1] = "(" + str(self.analyze(self.reanalyze([None,None,line.split()[2]])[1])) + ")"
                    if line.split()[0] == "if":
                        if line.split()[2] == "=":
                            if self.analyze(self.reanalyze([None,None,line.split()[1]])[1]) != self.analyze(self.reanalyze([None,None,line.split()[3]])[1]): do = False
                        if line.split()[2] == ">":
                            if self.analyze(self.reanalyze([None,None,line.split()[1]])[1]) <= self.analyze(self.reanalyze([None,None,line.split()[3]])[1]): do = False
                        if line.split()[2] == "<":
                            if self.analyze(self.reanalyze([None,None,line.split()[1]])[1]) >= self.analyze(self.reanalyze([None,None,line.split()[3]])[1]): do = False
                    if line.split()[0] == "return" and do:
                        return self.analyze(self.reanalyze([None,None,line.split()[1]])[1]) 
                    if line.split()[0] == "end": 
                        if line.split()[1] == "if": do = True
                    if line.split()[0] == "goto" and do:
                        for g in self.gotos:
                            if line.split()[1] == g[0]: number = g[1] - 1
                else:
                    if line == "break" and do: 
                        return False
                    elif line == "else": do = not do

            else: 
                if do: self.run_instruction(line)
            number += 1
            

    def run_instruction(self, l):
        inst = l[0]
        param = l[1:]

        for i in self.commands:
            if i[0] == inst: 
                return i[1](self.convert(param))

    def convert(self, p):
        r = []
        for s in p:
            r.append(self.analyze(s))
        return r

    def analyze(self, s):     
        if s[0] == '(' and s[-1] == ')': 
            try:
                return int(s[1:-1])
            except ValueError:
                return s[1:-1]
        else:
            return self.find_var(s)

    def find_var(self,v):
        for var in self.variables:
            if var[0] == v: return self.analyze(var[1])

    def find_var_number(self,v):
        i = 0
        for var in self.variables:
            if var[0] == v: return i
            i += 1
        return

    def to_command(self, c):
        r = []
        w = ""
        cl = [":",";"]
        for l in c:
            if l == cl[0]:
                r.append(w)
                w = ""
                continue 
            if l == cl[1]:
                r.append(w)
                return r
            w += l

    def reanalyze(self, v):
        if self.to_command(v[2]) != None: 
            return [v[0],"(" + str(self.run_instruction(self.to_command(v[2]))) + ")"]
        else: return [v[0],v[2]]





def clean(t):
    r = []
    for p in t: 
        if p != None and p != "": r.append(p)
    return r


def notabs(se):
    w = ""
    s = 0
    i = 0
    p = True
    for c in se:
        if p:
            if c != " ":
                p = False
                w += c
        else:
            w += c


    return w

