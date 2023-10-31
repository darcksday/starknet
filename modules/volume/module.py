from loguru import logger
from termcolor import cprint
from helpers.cli import sleeping
from helpers.common import get_private_keys_recipients
from helpers.starknet import Starknet
from modules.exchange_withdraw.functions import find_starknet_network
from modules.volume.functions import run_one_wallet_volume


def run_volume_wallet_by_wallet():
    logger.info("Start volume module: wallet-by-wallet: OKX > ZkLend > AVNU/SithSwap > ZkLend > OKX")
    token = 'ETH'

    try:
        cex_network = find_starknet_network(token, False)
        wallet_list = get_private_keys_recipients()
    except Exception as e:
        logger.error(f'Error: {e}')
        raise SystemExit

    try:
        for _id, wallet in enumerate(wallet_list):
            account = Starknet(wallet['index'], wallet)
            run_one_wallet_volume(account, wallet['recipient'], cex_network)

            if _id < len(wallet_list) - 1:
                sleeping(100, 120)

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
