from common import TOKEN_ADDRESS
from modules.swaps.functions.avnu import swap_token_avnu
from modules.swaps.functions.jediswap import swap_token_jediswap
from modules.swaps.functions.myswap import swap_token_myswap
from modules.swaps.functions.open_ocean import swap_token_open_ocean
from modules.swaps.functions.protoss import swap_token_protoss
from modules.swaps.functions.sithswap import swap_token_sithswap
from modules.swaps.functions.tenk_swap import swap_token_10kswap

SWAP_ROUTES = {
    'swap_token_jediswap': {
        'tokens': {
            TOKEN_ADDRESS['USDC'],
            TOKEN_ADDRESS['WBTC'],
            TOKEN_ADDRESS['DAI'],
            TOKEN_ADDRESS['USDT']
        },
        'function': swap_token_jediswap
    },
    'swap_token_avnu': {
        'tokens': {
            TOKEN_ADDRESS['USDC'],
            TOKEN_ADDRESS['WBTC'],
            TOKEN_ADDRESS['DAI'],
            TOKEN_ADDRESS['USDT']
        },
        'function': swap_token_avnu
    },
    'swap_token_myswap': {
        'tokens': {
            TOKEN_ADDRESS['USDC'],
            TOKEN_ADDRESS['WBTC'],
            TOKEN_ADDRESS['DAI'],
            TOKEN_ADDRESS['USDT']
        },
        'function': swap_token_myswap
    },
    'swap_token_protoss': {
        'tokens': {
            TOKEN_ADDRESS['USDC'],
            TOKEN_ADDRESS['DAI'],
            TOKEN_ADDRESS['USDT']
        },
        'function': swap_token_protoss
    },
    'swap_token_sithswap': {
        'tokens': {
            TOKEN_ADDRESS['USDC'],
            TOKEN_ADDRESS['WBTC'],
            TOKEN_ADDRESS['DAI'],
            TOKEN_ADDRESS['USDT']
        },
        'function': swap_token_sithswap
    },
    'swap_token_10kswap': {
        'tokens': {
            TOKEN_ADDRESS['USDC'],
            TOKEN_ADDRESS['WBTC'],
            TOKEN_ADDRESS['DAI'],
            TOKEN_ADDRESS['USDT']
        },
        'function': swap_token_10kswap
    },
    # 'swap_token_open_ocean': {
    #     'tokens': {
    #         TOKEN_ADDRESS['USDC'],
    #         TOKEN_ADDRESS['WBTC'],
    #         TOKEN_ADDRESS['DAI'],
    #         TOKEN_ADDRESS['USDT']
    #     },
    #     'function': swap_token_open_ocean
    # },

}
