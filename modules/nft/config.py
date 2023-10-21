import json

STARKNET_ID_CONTRACT = 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af

STARKVERSE_CONTRACT = 0x060582df2cd4ad2c988b11fdede5c43f56a432e895df255ccd1af129160044b8

PYRAMID_CONTRACT = 0x042e7815d9e90b7ea53f4550f74dc12207ed6a0faaef57ba0dbf9a66f3762d82

UNFRAMED_CONTRACT = 0x051734077ba7baf5765896c56ce10b389d80cdcee8622e23c0556fb49e82df1b

with open('abi/starknet_id/abi.json') as file:
    STARKNET_ID_ABI = json.load(file)

with open('abi/pyramid/abi.json') as file:
    PYRAMID_ABI = json.load(file)

with open('abi/unframed/abi.json') as file:
    UNFRAMED_ABI = json.load(file)
