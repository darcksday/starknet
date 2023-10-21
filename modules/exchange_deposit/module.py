from loguru import logger

from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import print_input_amounts_range, sleeping
from helpers.common import get_private_keys_recipients
from helpers.starknet import Starknet
from modules.exchange_withdraw.cli import *
from modules.exchange_deposit.functions import transfer_eth


def interface_transfer_to_exchange():
    amount_str = print_input_amounts_range('Transfer ETH amount')
    try:
        keys_with_recipients = get_private_keys_recipients()
    except Exception as e:
        logger.error(f'Error: {e}')
        raise SystemExit

    for _id, wallet in enumerate(keys_with_recipients):
        account = Starknet(_id, wallet)
        amount = get_amount_in_range(amount_str)

        transfer_eth(account, wallet['recipient'], amount)

        if _id < len(keys_with_recipients) - 1:
            sleeping(MIN_SLEEP, MAX_SLEEP)
