import json

with open('abi/jediswap/abi.json') as file:
    JEDISWAP_ABI = json.load(file)

with open('abi/myswap/abi.json') as file:
    MYSWAP_ABI = json.load(file)

with open('abi/10kswap/abi.json') as file:
    STARKSWAP_ABI = json.load(file)

with open('abi/sithswap/abi.json') as file:
    SITHSWAP_ABI = json.load(file)

with open('abi/protoss/abi.json') as file:
    PROTOSS_ABI = json.load(file)

MYSWAP_POOLS = {
    "ETHUSDC": 1,
    "DAIETH": 2,
    "WBTCUSDC": 3,
    "ETHUSDT": 4,
    "USDCUSDT": 5,
    "DAIUSDC": 6
}

JEDISWAP_CONTRACT = 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023

MYSWAP_CONTRACT = 0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28

STARKSWAP_CONTRACT = 0x07a6f98c03379b9513ca84cca1373ff452a7462a3b61598f0af5bb27ad7f76d1

SITHSWAP_CONTRACT = 0x28c858a586fa12123a1ccb337a0a3b369281f91ea00544d0c086524b759f627

PROTOSS_CONTRACT = 0x07a0922657e550ba1ef76531454cb6d203d4d168153a0f05671492982c2f7741

AVNU_CONTRACT = 0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f
