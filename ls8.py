import sys
from cpu import Cpu

cpu = Cpu()

if len(sys.argv) != 2:
    print("usage: ls8.py <filename>", file=sys.stderr)
    sys.exit(1)
else:
    cpu.load(sys.argv[1])
    cpu.run()
