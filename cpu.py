import sys


class Cpu:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.fl = [0] * 8

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0

            with open(filename) as file:
                for instruction in file:
                    splitted_instruction = instruction.split("#")
                    binary_num = splitted_instruction[0].strip()
                    try:
                        if binary_num is not None:
                            result = int(binary_num)
                            self.ram_write(address, result)
                            address += 1
                    except ValueError:
                        continue

        except FileNotFoundError:
            print(f"{sys.argv[0]} : {sys.argv[1]} file not found")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        LDI = 0b10000010
        CMP = 0b10100111
        JEQ = 0b01010101
        PRN = 0b01000111
        JNE = 0b01010110
        JMP = 0b01010100
        HLT = 0b00000001

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            op_code = int(f"0b{IR}", 2)

            if op_code == LDI:
                self.reg[int(f'{operand_a}', 2)] = int(f'{operand_b}', 2)

                shift = op_code
                incr = shift >> 6
                self.pc += (incr + 1)

            elif op_code == CMP:
                if self.reg[int(f"{operand_a}", 2)] < self.reg[int(f"{operand_b}", 2)]:
                    self.fl[5] = 1
                elif self.reg[int(f"{operand_a}", 2)] > self.reg[int(f"{operand_b}", 2)]:
                    self.fl[6] = 1
                elif self.reg[int(f"{operand_a}", 2)] == self.reg[int(f"{operand_b}", 2)]:
                    self.fl[7] = 1

                shift = op_code
                incr = shift >> 6
                self.pc += (incr + 1)

            elif op_code == JEQ:
                if self.fl[7] == 1:
                    self.pc = self.reg[int(f'{operand_a}', 2)]

                else:
                    shift = op_code
                    incr = shift >> 6
                    self.pc += (incr + 1)

            elif op_code == PRN:
                print(self.reg[int(f"{operand_a}", 2)])

                shift = op_code
                incr = shift >> 6
                self.pc += (incr + 1)

            elif op_code == JNE:
                if self.fl[7] == 0:
                    self.pc = self.reg[int(f'{operand_a}', 2)]
                else:
                    shift = op_code
                    incr = shift >> 6
                    self.pc += (incr + 1)

            elif op_code == JMP:
                self.pc = self.reg[int(f'{operand_a}', 2)]

            elif op_code == HLT:
                sys.exit(1)
