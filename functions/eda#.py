class CPU:

    def __init__(self) -> None:
        self.MEM = {}
        self.REG = {}
        self.PC = 1
        self.IR = None
        self.POS = 0
        self.ANGL = 0

    def STORE(self, M1, v):
        self.MEM[M1] = v

    def LOAD(self, R, M):
        self.REG[R] = self.MEM[M]

    def LOADI(self, R, v):
        self.REG[R] = v

    def ADDI(self, dest, src1, v):
        self.REG[dest] = self.REG[src1] + v

    def BEQ(self, R1, R2, LAB):
        if self.REG[R1] == self.REG[R2]:
            self.PC = LAB

    def J(self, LAB):
        self.PC = LAB

    def AV(self, X):
        self.POS += X

    def TD(self):
        self.ANGL -= 90

    def RUN(self, code):
        while code[self.PC] != "END":
            print(f"REG: {self.REG}, PC: {self.PC}, POS: {self.POS}, ANGL: {self.ANGL}")
            input("$ hit Enter to proceed")
            self.IR = code[self.PC]
            self.PC += 1
            self.IR()
        print(f"REG: {self.REG}, PC: {self.PC}, POS: {self.POS}, ANGL: {self.ANGL}")


def lexxer(code:str)->list:
    """
    Returns the code as a list of instructions, that can get compiled
    """
    prog = []
    temp = ""
    for i in range(len(code)):
        temp += code[i]
        if temp == "if(":
            ...
        elif temp == "av(":
            count = 1
            while True:
                i+= 1
                if code[i].isdigit():
                    count = int(code[i])*(10**(len(str(count))-1))
                elif code[i] == ")":
                    prog.append({"av":count})
                    break
        elif code[i] in ["{",";"]:
            temp = ""
        elif temp == "td()":
            prog.append({"td":[]})
        elif temp == "}":
            prog.append({"endrepeat":[]})
    return prog


def compiler(instr:list)->dict[int, function]:
    """
    Returns the Assembly code of the instructions, that can get executed
    """
    ...