import gdb
import shlex
import string

avoid1 = [0x40071d, 0x40077a, 0x4007d7, 0x400834, 0x400894, 0x4008f4, 0x400950, 0x4009a8, 0x400a09, 0x400a6f, 0x400ac7, 0x400b24, 0x400b81, 0x400bd9, 0x400c31, 0x400c8e, 0x400ce6, 0x400d3e, 0x400d96, 0x400df2, 0x400e4a, 0x400ea0, 0x400eeb]
avoid2 = [0x400fb3, 0x4010ba, 0x4011bc, 0x4012be, 0x4013c6, 0x4014d4, 0x4015d6, 0x4016c0, 0x4017c2, 0x4018c4, 0x4019cd, 0x401ab7, 0x401bb9, 0x401cc5, 0x401db2, 0x401eba, 0x401fbc, 0x4020c2, 0x4021c4, 0x4022cb, 0x4023ba, 0x4024bc, 0x4025c3, 0x4026b2, 0x402c20]
avoid = avoid1 + avoid2 + [0x402727] # return from function (dummy breakpoint)

charset = "{}_?" + string.digits + string.ascii_letters
flag = [' '] * 32

def brute(i):
  global flag
  global last_breakpoint
  for c in charset:
    flag[i] = c
    output = gdb.execute('r < <(echo {})'.format(shlex.quote(''.join(flag))), True, True)
    # skip floating point exception
    while "SIGFPE" in output:
      output = gdb.execute('c', True, True)

    output = gdb.execute('x $pc', True, True)
    pc = output.split(":")[0]
    pc = int(pc, 16)
    if pc > last_breakpoint:
      last_breakpoint = pc
      break
  print(''.join(flag))

gdb.execute('file no_flo')

gdb.execute('delete breakpoints')
for a in avoid:
  gdb.execute('b *{}'.format(hex(a)))
last_breakpoint = avoid1[0]
for i in range(0, 32, 2):
  brute(i)

gdb.execute('delete breakpoints')
for a in avoid:
  gdb.execute('b *{}'.format(hex(a)))
last_breakpoint = avoid2[0]
for i in range(1, 32, 2):
  brute(i)

quit()
