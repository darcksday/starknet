import json

ZETH_TOKEN_ADDRESS = 0x01b5bd713e72fdc5d63ffd83762f81297f6175a5e0a4771cdadbc1dd5fe72cb1

TOKEN_ADDRESS = {
    "ETH": 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
    "USDC": 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
    "USDT": 0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8,
    "DAI": 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3,
    "WBTC": 0x03fe2b97c1fd336e750087d68b9b867997fd64a2661ff3ca5a7c771641e8e7ac
}

BRAAVOS_PROXY_CLASS_HASH = 0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e
BRAAVOS_IMPLEMENTATION_CLASS_HASH = 0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570

ARGENTX_PROXY_CLASS_HASH = 0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918
ARGENTX_IMPLEMENTATION_CLASS_HASH = 0x33434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2
ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW = 0x01a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003

with open('abi/rpc.json') as file:
    RPC = json.load(file)

with open('abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

CHAINS = {
    'ethereum': {
        'rpc': 'https://rpc.ankr.com/eth',
        'explorer': 'https://etherscan.io/tx',
        'token': 'ETH',
        'chain_id': 1
    },
    'optimism': {
        'rpc': 'https://opt-mainnet.g.alchemy.com/v2/ZlBxXxXF5NNbl7kcRzvOs8V8XnRRhT3W',
        'explorer': 'https://optimistic.etherscan.io/tx',
        'token': 'ETH',
        'chain_id': 10
    },
    'arbitrum': {
        'rpc': 'https://rpc.ankr.com/arbitrum',
        'explorer': 'https://arbiscan.io/tx',
        'token': 'ETH',
        'chain_id': 42161
    },
    'zksync': {
        'rpc': 'https://mainnet.era.zksync.io',
        'explorer': 'https://explorer.zksync.io/tx',
        'token': 'ETH',
        'chain_id': 324
    },
    'linea': {
        'rpc': 'https://linea-mainnet.infura.io/v3/7064390927dd49ebbf576d876293842d',
        'explorer': 'https://lineascan.build/tx',
        'token': 'ETH',
        'chain_id': 59144
    },
}
