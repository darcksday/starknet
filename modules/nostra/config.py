import json

from helpers.common import int_to_wei

NOSTRA_CONTRACTS = {
    "ETH": 0x07170f54dd61ae85377f75131359e3f4a12677589bb7ec5d61f362915a5c0982,
    "USDC": 0x06eda767a143da12f70947192cd13ee0ccc077829002412570a88cd6539c1d85,
    "DAI": 0x04f18ffc850cdfa223a530d7246d3c6fc12a5969e0aa5d4a88f470f5fe6c46e9,
    "USDT": 0x0453c4c996f1047d9370f824d68145bd5e7ce12d00437140ad02181e1d11dc83,
}

NOSTRA_DEPOSIT_LIMITS = {
    "ETH": int_to_wei(0.004, 18),
    "USDC": int_to_wei(5, 6),
    "DAI": int_to_wei(5, 18),
    "USDT": int_to_wei(5, 6),
}

with open('abi/nostra/abi.json') as file:
    NOSTRA_ABI = json.load(file)