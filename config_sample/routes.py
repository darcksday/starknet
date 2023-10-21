from helpers.factory import run_random_swap
from modules.dmail.module import dmail_send_email
from modules.nft.functions.pyramid import nft_pyramid
from modules.nft.functions.starknet_id import nft_starknet_id
from modules.nft.functions.starkverse import nft_starkverse
from modules.nft.functions.unframed import nft_unframed
from modules.zklend.functions.zklend_collateral import zklend_collateral_enable
from modules.zklend.functions.zklend_deposit import zklend_deposit
from modules.zklend.functions.zklend_withdraw import zklend_withdraw

"""
You can use:
nft_pyramid
nft_starknet_id
nft_starkverse
nft_unframed
run_random_swap
dmail_send_email
zklend_collateral_enable
zklend_deposit
zklend_withdraw

______________________________________________________

You can add functions to [], for example: 
[module_1, module_2, [module_3, module_4], module 5]
The script will start module 3 and 4 sequentially, others modules 
module_1, module_2 and module_5 will start randomly.

You can duplicate function for example: [run_random_swap, run_random_swap, run_random_swap]
for swaps in different protocols

"""

USE_MULTIPLE_FUNCTIONS = [
    nft_pyramid,
    nft_starknet_id,
    nft_starkverse,
    nft_unframed,
    [
        zklend_deposit,
        zklend_withdraw,
    ],
    run_random_swap,
    run_random_swap,
    run_random_swap,
    dmail_send_email,
    zklend_collateral_enable,
]
