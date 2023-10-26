from modules.swaps.config import *
from modules.nft.config import *
from modules.dmail.config import DMAIL_CONTRACT
from modules.dmail.module import dmail_send_email
from modules.nft.functions.pyramid import nft_pyramid
from modules.nft.functions.starknet_id import nft_starknet_id
from modules.nft.functions.starkverse import nft_starkverse
from modules.nft.functions.unframed import nft_unframed
from modules.swaps.functions.avnu import swap_token_avnu
from modules.swaps.functions.jediswap import swap_token_jediswap
from modules.swaps.functions.myswap import swap_token_myswap
from modules.swaps.functions.protoss import swap_token_protoss
from modules.swaps.functions.sithswap import swap_token_sithswap
from modules.swaps.functions.tenk_swap import swap_token_10kswap
from modules.zklend.config import ZKLEND_CONCTRACTS
from modules.zklend.functions.zklend_deposit import zklend_deposit
from modules.zklend.functions.zklend_withdraw import zklend_withdraw

ALL_CONTRACT_FUNCTIONS = {
    STARKNET_ID_CONTRACT: nft_starknet_id,
    STARKVERSE_CONTRACT: nft_starkverse,
    PYRAMID_CONTRACT: nft_pyramid,
    UNFRAMED_CONTRACT: nft_unframed,
    DMAIL_CONTRACT: dmail_send_email,
    JEDISWAP_CONTRACT: swap_token_jediswap,
    MYSWAP_CONTRACT: swap_token_myswap,
    STARKSWAP_CONTRACT: swap_token_10kswap,
    SITHSWAP_CONTRACT: swap_token_sithswap,
    PROTOSS_CONTRACT: swap_token_protoss,
    AVNU_CONTRACT: swap_token_avnu,
    ZKLEND_CONCTRACTS['router']: [zklend_deposit, zklend_withdraw],
}
