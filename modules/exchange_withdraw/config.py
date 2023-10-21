from dotenv import dotenv_values

config = dotenv_values("config/.env")

CEX_KEYS = {
    'okx': {
        'api_key': config['OKX_API_KEY'],
        'api_secret': config['OKX_API_SECRET'],
        'password': config['OKX_PASSWORD']
    },
    'okx-sub-1': {
        'api_key': config['OKX_SUB1_API_KEY'],
        'api_secret': config['OKX_SUB1_API_SECRET'],
        'password': config['OKX_SUB1_PASSWORD'],
        'name': config['OKX_SUB1_NAME'],
    },
    'okx-sub-2': {
        'api_key': config['OKX_SUB2_API_KEY'],
        'api_secret': config['OKX_SUB2_API_SECRET'],
        'password': config['OKX_SUB2_PASSWORD'],
        'name': config['OKX_SUB2_NAME'],
    },
    'okx-sub-3': {
        'api_key': config['OKX_SUB3_API_KEY'],
        'api_secret': config['OKX_SUB3_API_SECRET'],
        'password': config['OKX_SUB3_PASSWORD'],
        'name': config['OKX_SUB3_NAME'],
    },
    'okx-sub-4': {
        'api_key': config['OKX_SUB4_API_KEY'],
        'api_secret': config['OKX_SUB4_API_SECRET'],
        'password': config['OKX_SUB4_PASSWORD'],
        'name': config['OKX_SUB4_NAME'],
    },
    'okx-sub-5': {
        'api_key': config['OKX_SUB5_API_KEY'],
        'api_secret': config['OKX_SUB5_API_SECRET'],
        'password': config['OKX_SUB5_PASSWORD'],
        'name': config['OKX_SUB5_NAME'],
    },
}

CEX_DEFAULT_TOKENS = ['ETH']

OKX_CHAIN_MAPPING = {
    'ETH': 'ERC20',
}
