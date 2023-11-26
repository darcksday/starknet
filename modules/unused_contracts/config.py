from modules.deploy.config import STARKGUARDIANS_CONTRACT
from modules.deploy.functions import deploy_token
from modules.nft.functions.flex import nft_flex
from modules.nft.functions.gol2 import nft_gol2
from modules.nostra.config import NOSTRA_CONTRACTS
from modules.swaps.config import *
from modules.nft.config import *
from modules.dmail.config import DMAIL_CONTRACT
from modules.dmail.module import dmail_send_email
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
from modules.nostra.functions.nostra_deposit import nostra_deposit
from modules.nostra.functions.nostra_withdraw import nostra_withdraw

ALL_CONTRACT_FUNCTIONS = {
    STARKNET_ID_CONTRACT: nft_starknet_id,
    STARKVERSE_CONTRACT: nft_starkverse,
    UNFRAMED_CONTRACT: nft_unframed,
    FLEX_CONTRACT: nft_flex,
    DMAIL_CONTRACT: dmail_send_email,
    JEDISWAP_CONTRACT: swap_token_jediswap,
    MYSWAP_CONTRACT: swap_token_myswap,
    STARKSWAP_CONTRACT: swap_token_10kswap,
    SITHSWAP_CONTRACT: swap_token_sithswap,
    PROTOSS_CONTRACT: swap_token_protoss,
    AVNU_CONTRACT: swap_token_avnu,
    ZKLEND_CONCTRACTS['router']: [zklend_deposit, zklend_withdraw],
    NOSTRA_CONTRACTS['ETH']: [nostra_deposit, nostra_withdraw],
    GOL2_CONTRACT: nft_gol2,
    STARKGUARDIANS_CONTRACT: deploy_token,
}
