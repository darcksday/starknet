import json

with open('abi/starkguardians/abi.json') as file:
    STARKGUARDIANS_ABI = json.load(file)

STARKGUARDIANS_CONTRACT = 0x041a78e741e5af2fec34b695679bc6891742439f7afb8484ecd7766661ad02bf