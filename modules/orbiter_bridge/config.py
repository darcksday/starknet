import json

ORBITER_AMOUNT = {
    'ethereum': 0.000000000000009001,
    'optimism': 0.000000000000009007,
    'bsc': 0.000000000000009015,
    'arbitrum': 0.000000000000009002,
    'nova': 0.000000000000009016,
    'polygon': 0.000000000000009006,
    'polygon_zkevm': 0.000000000000009017,
    'zksync': 0.000000000000009014,
    'starknet': 0.000000000000009004,
    'linea': 0.000000000000009023,
}

ORBITER_NETWORKS = {
    "ethereum": 9001,
    "arbitrum": 9002,
    "starknet": 9004,
    "polygon": 9006,
    "optimism": 9007,
    "zksync": 9014,
    "bsc": 9015,
    "nova": 9016,
    "zkevm": 9017,
    "base": 9021,
}

ORBITER_CONTRACTS = {
    "bridge": "0xd9d74a29307cc6fc8bf424ee4217f1a587fbc8dc",
    "withdraw": 0x173f81c529191726c6e7287e24626fe24760ac44dae2a1f7e02080230f8458b
}

ORBITER_DEPOSIT_CONTRACTS = {
    'ethereum': '0xd9d74a29307cc6fc8bf424ee4217f1a587fbc8dc',
    'optimism': '0xd9d74a29307cc6fc8bf424ee4217f1a587fbc8dc',
    'arbitrum': '0xd9d74a29307cc6fc8bf424ee4217f1a587fbc8dc',
    'zksync': '0xBF3922a0cEBbcD718e715e83d9187cC4BbA23f11',
    'linea': '0xd9d74a29307cc6fc8bf424ee4217f1a587fbc8dc',
}

with open('abi/orbiter/deposit.json') as file:
    ORBITER_DEPOSIT_ABI = json.load(file)

with open('abi/orbiter/withdraw.json') as file:
    ORBITER_WITHDRAW_ABI = json.load(file)
