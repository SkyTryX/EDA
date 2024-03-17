from __future__ import annotations
from typing import Literal
from dataclasses import dataclass

class CPU:
    """
    les primitives du processeur LOAD, STORE, BLT...
    prennent toutes trois arguments
    pour faciliter le traitement
    les lettres z et t sont des variables vides
    """
    def __init__(self) -> None:
        self.POS = 0 # addresse mémoire
        self.ANGL = 1 # addresse mémoire
        self.MEM = {self.POS: 0, self.ANGL: 0}
        self.REG = {}
        self.PC = 1
        self.IR = None
        self.CMD = {}

    def temp_reg(self) -> None:
        """
        prend la plus petite clé libre dans proc.REG
        """
        return max(self.MEM.keys()) + 1
    
    def STORE(self, M1, X, z):
        self.MEM[M1] = self.REG[X]

    def LOAD(self, R, M, z):
        self.REG[R] = self.MEM[M]

    def LOADI(self, R, v, z):
        self.REG[R] = v

    def ADDI(self, dest, src1, v):
        self.REG[dest] = self.REG[src1] + v

    def BEQ(self, R1, R2, LAB):
        if self.REG[R1] == self.REG[R2]:
            self.PC = LAB

    def BLT(self, R1, R2, LAB):
        if self.REG[R1] < self.REG[R2]:
            self.PC = LAB

    def J(self, LAB,z,t):
        self.PC = LAB

    def register_cmd(self):
        self.CMD['STORE'] = self.STORE
        self.CMD['LOAD'] = self.LOAD
        self.CMD['LOADI'] = self.LOADI
        self.CMD['ADDI'] = self.ADDI
        self.CMD['BEQ'] = self.BEQ
        self.CMD['BLT'] = self.BLT
        self.CMD['J']= self.J

    def fetchdecode(self, code,line):
        x,y,z,t = code[line]
        return lambda:self.CMD[x](y,z,t)

    # à réécrire vu que dans l'ASM je mets juste le op_code ('LOADI')
    def RUN(self, code):
        self.register_cmd()
        while self.PC < len(code):
            self.IR = self.fetchdecode(code,self.PC)
            self.PC += 1
            self.IR()
            print(f"REG: {self.REG}, PC: {self.PC}, POS: {self.POS}, ANGL: {self.ANGL}")
            input("$ hit Enter to proceed")

OP_CODE = Literal['REPEAT', 'AV', 'TD', 'TG', 'IFTHENELSE']

class NOOP:
    """the empty ast"""
    pass

@dataclass
class OP:
    op_code: OP_CODE 
    args: tuple[int, list[OP]]

ast = OP('REPEAT', (7,[
    OP('AV', (1, [])), 
    OP('TD',(0, [])),
    OP('AV',(2,[])),
    OP('TG',(0,[])),
    OP('TG',(0,[])),
        ])
        )

class ASM:
    """
    prog in assembly code
    ex:
    prog = {
    1: ('LOADI',0,0,),
    2: ('LOADI',1,3,), 
    3: ('LOADI',2,2,),
    4: ('BEQ',0,1,9),
    5: ('ADDI',1,1,-1),
    8: ('J',4,,),
    9: ('NOOP',,,)
    }
    """

    def __init__(self, c: CPU) -> None:
        self.cpu = c
        self.prog = {}
     
def ordine(prog: OP, proc: CPU) -> ASM:
    """attribue les numéros de lignes ?"""

    pass

def compile(source: OP, p: CPU) -> ASM:
    asm = ASM(p)
    TEMP = p.temp_reg() # addresse registre temporaire
    match source:
        case OP(op_code='AV', args=(X,_)):
            asm.prog[1] = ('LOAD', TEMP, p.POS,0)
            asm.prog[2] = ('ADDI', TEMP, TEMP,X)
            asm.prog[3] = ('STORE', p.POS, TEMP,0)
        case OP(op_code='TD', args=_ ):
            asm.prog[1] = ('LOAD', TEMP, p.ANGL,0)
            asm.prog[2] = ('ADDI', TEMP, TEMP, -90)
            asm.prog[3] = ('STORE', p.ANGL, TEMP,0)
        case OP(op_code='TG', args=_ ):
            asm.prog[1] = ('LOAD', TEMP, p.ANGL,0)
            asm.prog[2] = ('ADDI', TEMP, TEMP, 90)
            asm.prog[3] = ('STORE', p.ANGL, TEMP,0)
    return asm