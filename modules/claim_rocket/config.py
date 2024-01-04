import json

with open('abi/rocket/abi.json') as file:
    ROCKER_ABI = json.load(file)

CLAIM_CONTRACT = 0x01c50d0cd1ee43c43e0d9059cb707bfabe532564431fe8badb9c8b79ef928bed
