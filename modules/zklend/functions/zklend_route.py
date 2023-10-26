import random
import time

from loguru import logger
from common import TOKEN_ADDRESS, ZETH_TOKEN_ADDRESS
from config.settings import MIN_SLEEP, MAX_SLEEP, MIN_BALANCE_ETH
from helpers.cli import sleeping
from helpers.common import wei_to_int
from helpers.factory import run_script_one
from helpers.starknet import Starknet
from modules.volume.helpers import check_wait_wallet_balance
from modules.zklend.functions.zklend_borrow import zklend_borrow_stable, get_max_borrow_amount
from modules.zklend.functions.zklend_collateral import zklend_collateral_enable
from modules.zklend.functions.zklend_deposit import zklend_deposit
from modules.zklend.functions.zklend_repay import zklend_repay_stable
from modules.zklend.functions.zklend_withdraw import zklend_withdraw


def zklend_route(account: Starknet, amount: float):
    eth_balance = wei_to_int(account.get_eth_balance())

    max_eth_to_use = eth_balance - 0.0012 - MIN_BALANCE_ETH
    if max_eth_to_use <= 0:
        logger.error(
            f"[{account._id}][{account.address_original}] Not enough ETH, balance: {eth_balance} ETH, need: {max_eth_to_use}")
        return

    if not amount or amount > max_eth_to_use:
        amount = max_eth_to_use

    logger.info(f"[{account._id}][{account.address_original}] Amount: {amount} ETH")

    # Deposit ETH
    run_script_one(account, zklend_deposit, str(amount), [TOKEN_ADDRESS['ETH']], 'zklend_route')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # Enable ETH collateral
    run_script_one(account, zklend_collateral_enable, "", [TOKEN_ADDRESS['ETH']], 'zklend_route')

    check_wait_wallet_balance(account, amount * 0.99, 'zETH', ZETH_TOKEN_ADDRESS)
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # Borrow random token
    random_token_symbol = random.choice(["USDC", "USDT", "DAI"])
    random_token = TOKEN_ADDRESS[random_token_symbol]
    max_borrow = get_max_borrow_amount(account, random_token_symbol)
    run_script_one(account, zklend_borrow_stable, "0", [random_token], 'zklend_route')

    check_wait_wallet_balance(account, max_borrow * 0.99, random_token_symbol, random_token)
    sleeping(MIN_SLEEP * 2, MAX_SLEEP * 2)

    # Repay token
    balance_before_repay = account.get_balance(random_token)['balance']
    run_script_one(account, zklend_repay_stable, "0", [random_token], 'zklend_route')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    while True:
        balance = account.get_balance(random_token)['balance']
        if balance < balance_before_repay:
            break
        time.sleep(5)
        continue

    # Withdraw ETH
    run_script_one(account, zklend_withdraw, "0", [TOKEN_ADDRESS['ETH']], 'zklend_route')
