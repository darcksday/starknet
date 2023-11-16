from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import get_private_keys
from helpers.starknet import Starknet
from modules.unused_contracts.functions import run_random_unused_function
from loguru import logger


def interface_unused_contracts():
    prt_keys = get_private_keys()
    for _id, wallet in enumerate(prt_keys):
        account = Starknet(wallet["index"], wallet)

        if not account.address_original:
            logger.error(f'No "starknet_address" provided in config/wallets.csv, skip.')
            continue

        need_sleep = run_random_unused_function(account)

        if _id < len(prt_keys) - 1 and need_sleep:
            sleeping(MIN_SLEEP, MAX_SLEEP)
