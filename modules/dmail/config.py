import json

with open('abi/dmail/abi.json') as file:
    DMAIL_ABI = json.load(file)

DMAIL_CONTRACT = 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309
