from loguru import logger

from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import get_private_keys
from modules.exchange_withdraw.cli import *
from modules.exchange_withdraw.functions import call_exchange_withdraw, find_starknet_network


def interface_exchange_withdraw():
    token = 'ETH'

    try:
        network = find_starknet_network(token)
    except Exception as err:
        logger.error(str(err), 'red')
        return

    wallet_list = get_private_keys()
    amount_str = print_exchange_withdraw_amount()

    if print_approve_transaction(amount_str, wallet_list):
        for _id, wallet in enumerate(wallet_list):
            amount = get_amount_in_range(amount_str)
            call_exchange_withdraw(wallet['starknet_address'], network, amount, token)

            if _id < len(wallet_list) - 1:
                sleeping(MIN_SLEEP, MAX_SLEEP)
