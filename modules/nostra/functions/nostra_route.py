from loguru import logger
from common import TOKEN_ADDRESS
from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import get_min_balance_eth, wei_to_int
from helpers.factory import run_script_one
from helpers.starknet import Starknet
from modules.nostra.functions.nostra_deposit import nostra_deposit
from modules.nostra.functions.nostra_withdraw import nostra_withdraw


def nostra_route(account: Starknet, amount: float):
    eth_balance = wei_to_int(account.get_eth_balance())
    max_eth_to_use = eth_balance - 0.0008 - get_min_balance_eth()

    if max_eth_to_use <= 0:
        logger.error(
            f"[{account._id}][{account.address_original}] Not enough ETH, balance: {eth_balance} ETH, need: {max_eth_to_use}")
        return

    if not amount or amount > max_eth_to_use:
        amount = max_eth_to_use

    logger.info(f"[{account._id}][{account.address_original}] Amount: {amount} ETH")

    # Deposit ETH
    run_script_one(account, nostra_deposit, str(amount), [TOKEN_ADDRESS['ETH']], 'nostra_route')
    sleeping(MIN_SLEEP * 2, MAX_SLEEP * 2)

    #Withdraw ETH
    run_script_one(account, nostra_withdraw, "0", [TOKEN_ADDRESS['ETH']], 'nostra_route')
