import sys

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
    
# Switch Case ------------------------------------------------------------------------------------------------------------
    def execute(self, op):
        while self.pc < len(op):
            print("pc =", self.pc)
            if op[self.pc][0] == 'movi':
                self.movi(op[self.pc][1])
                
            elif op[self.pc][0] == 'mov':
                self.mov(op[self.pc][1])

            elif op[self.pc][0] == 'add':
                self.add(op[self.pc][1])

            elif op[self.pc][0] == 'addi':
                self.addi(op[self.pc][1])

            elif op[self.pc][0] == 'sub':
                self.sub(op[self.pc][1])
                
            elif op[self.pc][0] == 'subi':
                self.subi(op[self.pc][1])
                
            elif op[self.pc][0] == 'mul':
                self.mul(op[self.pc][1])
                
            elif op[self.pc][0] == 'div':
                self.div(op[self.pc][1])

            elif op[self.pc][0] == 'blt':
                self.pc = self.blt(op[self.pc][1])
            
            elif op[self.pc][0] == 'bgt':
                self.pc = self.bgt(op[self.pc][1])
                
            elif op[self.pc][0] == 'beq':
                self.pc = self.beq(op[self.pc][1])
                
            elif op[self.pc][0] == 'j':
                self.pc = self.j(op[self.pc][1])
                
            elif op[self.pc][0] == 'jr':
                self.pc = self.jr(op[self.pc][1])
                
            elif op[self.pc][0] == 'jal':
                self.pc = self.jal(op[self.pc][1])

            elif op[self.pc][0] == 'sw':
                self.sw(op[self.pc][1])

            elif op[self.pc][0] == 'lw':
                self.lw(op[self.pc][1])

            self.pc += 1
            print("--------------------")
    
# Instruções de Movimentação ----------------------------------------------------------------------------------------------
    def movi(self, reg):
        self.registradores[reg[0]] = int(reg[1])
        print(f'{reg[0]} = {self.registradores[reg[0]]}')
        
    def mov(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]]
        print(f'{reg[0]} = {reg[1]} = {self.registradores[reg[0]]}')

# Instruções Aritméticas --------------------------------------------------------------------------------------------------
    def add(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]] + self.registradores[reg[2]]
        print(f'{reg[0]} = {reg[1]} + {reg[2]} = {self.registradores[reg[0]]}')
    
    def addi(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]] + int(reg[2])
        print(f'{reg[0]} = {reg[1]} + {int(reg[2])} = {self.registradores[reg[0]]}')
        
    def sub(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]] - self.registradores[reg[2]]
        print(f'{reg[0]} = {reg[1]} - {reg[2]} = {self.registradores[reg[0]]}')
        
    def subi(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]] - int(reg[2])
        print(f'{reg[0]} = {reg[1]} - {int(reg[2])} = {self.registradores[reg[0]]}')
    
    def mul(self, reg):
        self.registradores[reg[0]] = self.registradores[reg[1]] * self.registradores[reg[2]]
        print(f'{reg[0]} = {reg[1]} * {self.registradores[reg[2]]} = {self.registradores[reg[0]]}')
        
    def div(self, reg):
        if self.registradores[reg[2]] == 0:
            print("Erro: Divisão por zero")
            return
        self.registradores[reg[0]] = self.registradores[reg[1]] / self.registradores[reg[2]]
        print(f'{reg[0]} = {reg[1]} / {int(reg[2])} = {self.registradores[reg[0]]}')

# Instruções de Desvio ---------------------------------------------------------------------------------------------------
    def blt(self, reg):
        if self.registradores[reg[0]] < self.registradores[reg[1]]:
            print(f'jump to {int(reg[2])}')
            return int(reg[2]) - 1
        else:
            return self.pc
        
    def bgt(self, reg):
        if self.registradores[reg[0]] > self.registradores[reg[1]]:
            print(f'jump to {int(reg[2])}')
            return int(reg[2]) - 1
        else:
            return self.pc
        
    def beq(self, reg):
        if self.registradores[reg[0]] == self.registradores[reg[1]]:
            print(f'jump to {int(reg[2])}')
            return int(reg[2]) - 1
        else:
            return self.pc
        
    def j(self, reg):
        print(f'jump to {int(reg[0])}')
        return int(reg[0]) - 1
    
    def jr(self, reg):
        print(f'jump to {self.registradores[reg[0]]}')
        return self.registradores[reg[0]] - 1
    
    def jal(self, reg):
        self.ra = self.pc
        print("ra =", self.ra)
        print(f'jump to {int(reg[0])}')
        return int(reg[0]) - 1

# Instruções de Memória --------------------------------------------------------------------------------------------------
    def sw(self, reg):
        vimm = reg[1].split("(")
        rt = vimm[1].replace(")", "")
        self.mem[int(vimm[0])+self.registradores[rt]] = self.registradores[reg[0]]
        print(f'mem[{int(vimm[0])+self.registradores[rt]}] = {self.registradores[reg[0]]}')

    def lw(self, reg):
        vimm = reg[1].split("(")
        rs = vimm[1].replace(")", "")
        self.registradores[reg[0]] = self.mem[int(vimm[0]) + self.registradores[rs]]
        print(f'{reg[0]} = mem[{int(vimm[0])+self.registradores[rs]}] = {self.mem[int(vimm[0])+self.registradores[rs]]}')

# Execução do programa --------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    list_op = []                                     
    with open(sys.argv[1], 'r') as f:
        cpu = CPU()
        for line in f:
            operation = line.replace('\n', '').split(" ")
            operation[1] = operation[1].split(",")
            list_op.append(operation)
        cpu.execute(list_op)
        for i in range(8):
            r0,r8,r16,r24= 'r'+str(i),'r'+str(i+8),'r'+str(i+16),'r'+str(i+24)
            print(f'r{i}={cpu.registradores[r0]}\t\tr{i+8}={cpu.registradores[r8]}\t\tr{i+16}={cpu.registradores[r16]}\t\tr{i+24}={cpu.registradores[r24]}')
        for i in cpu.mem:
            if cpu.mem[i] != 0:
                print(f'mem[{i}] = {cpu.mem[i]}')
        print("--------------------")
        
