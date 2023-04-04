class CPU:
    def __init__(self):
        self.mem = [0]*2048
        self.pilha = {}
        self.pc = 0
        self.ra = 0
        self.sp = 0
        self.registradores = {}
        for i in range(32):
            self.registradores[f"r{i}"] = 0
    
    def execute(self, op):
        while self.pc < len(op):
            if op[self.pc][0] == 'movi':
                self.movi(op[self.pc][1])

            elif op[self.pc][0] == 'add':
                self.add(op[self.pc][1])

            elif op[self.pc][0] == 'addi':
                self.addi(op[self.pc][1])

            elif op[self.pc][0] == 'blt':
                self.pc = self.blt(op[self.pc][1])

            elif op[self.pc][0] == 'sw':
                self.sw(op[self.pc][1])

            elif op[self.pc][0] == 'lw':
                self.sw(op[self.pc][1])

            self.pc += 1
        
    def movi(self, reg):
        self.registradores[reg[0]] = int(reg[1])

    def add(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]] + self.registradores[reg[2]]
    
    def addi(self, reg):
        print(self.registradores[reg[1]], int(reg[2]))
        self.registradores[reg[0]] = self.registradores[reg[1]] + int(reg[2])

    def blt(self, reg):
        if self.registradores[reg[0]] < self.registradores[reg[1]]:
            return int(reg[2]) - 2
        else:
            return self.pc
        
    # def sw(self, reg):
    #     vimm = reg[1].split("(")
    #     rt = vimm[1].replace(")", "")
    #     #print(self.registradores["r11"],self.registradores["r2"])
    #     self.mem[int(vimm[0])+self.registradores[rt]] = self.registradores[reg[0]]

    # def lw(self, reg):
    #     vimm = reg[1].split("(")
    #     rs = vimm[1].replace(")", "")
    #     #print(vimm[0],rs)
    #     self.registradores[reg[0]] = self.mem[int(vimm[0]) + self.registradores[rs]]

list_op = []
with open("loop.s", 'r') as f:
    cpu = CPU()
    for line in f:
        operation = line.replace('\n', '').split(" ")
        operation[1] = operation[1].split(",")
        list_op.append(operation)
    cpu.execute(list_op)
    print(cpu.registradores)
