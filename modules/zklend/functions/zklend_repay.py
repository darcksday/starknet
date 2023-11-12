import random

from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from starknet_py.serialization import TupleDataclass

from common import TOKEN_ADDRESS
from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import int_to_wei, wei_to_int, price_token, all_prices
from helpers.factory import run_script_one
from modules.swaps.module import function_by_index
from modules.swaps.swap_routes import SWAP_ROUTES
from modules.zklend.common import get_deposit_amount
from modules.zklend.config import ZKLEND_CONCTRACTS, ZKLEND_ABI


def zklend_repay_amount_all(account, token):
    zklend_contract = account.get_contract(ZKLEND_CONCTRACTS["router"], ZKLEND_ABI)
    user_debt: TupleDataclass = zklend_contract.functions["get_user_debt_for_token"].call_sync(
        account.address,
        token
    )
    return user_debt.debt


def buy_token_for_repay(account, token, token_balance_wei, need_amount_wei, token_decimals):
    logger.info(f"[{account._id}][{account.address_original}]: Buy token to cover repay amount")

    diff_amount_wei = need_amount_wei - token_balance_wei
    # Get 2% more tokens to cover full borrow amount
    diff_amount_wei *= 1.02
    diff_amount = wei_to_int(diff_amount_wei, token_decimals)

    eth_price = price_token(all_prices(), "ETH")
    amount = diff_amount / float(eth_price)
    swap_function = function_by_index(random.randint(1, len(SWAP_ROUTES)))

    run_script_one(account, swap_function, str(amount), [TOKEN_ADDRESS['ETH'], token], 'buy_token_for_repay')


def zklend_repay_stable(account, amount: float = 0, token=None):
    if not token:
        token = TOKEN_ADDRESS["USDC"]

    token_decimals = account.get_balance(token)["decimal"]
    token_balance_wei = get_deposit_amount(account, token)
    max_repay_amount_wei = zklend_repay_amount_all(account, token)

    if not amount:
        amount_wei = max_repay_amount_wei
        function_name = "repay_all"
        repay_call_data = [token]
    else:
        amount_wei = int_to_wei(amount, token_decimals)
        function_name = "repay"
        repay_call_data = [token, amount_wei]

    if 0 < amount_wei <= max_repay_amount_wei:
        if token_balance_wei < amount_wei:
            # Buy tokens in random dex
            buy_token_for_repay(account, token, token_balance_wei, amount_wei, token_decimals)
            sleeping(MIN_SLEEP, MAX_SLEEP)
            token_balance_wei = get_deposit_amount(account, token)

        logger.info(f"[{account._id}][{account.address_original}]: ZkLend Repay")

        approve_contract = account.get_contract(token)
        approve_call = approve_contract.functions["approve"].prepare(
            ZKLEND_CONCTRACTS["router"],
            token_balance_wei
        )

        repay_call = Call(
            to_addr=ZKLEND_CONCTRACTS["router"],
            selector=get_selector_from_name(function_name),
            calldata=repay_call_data,
        )

        transaction = account.sign_transaction([approve_call, repay_call])
        transaction_response = account.send_transaction(transaction)
        if transaction_response:
            return transaction_response.transaction_hash
    else:
        error = f"Wrong amount: {amount} {f'is more than borrowed {wei_to_int(max_repay_amount_wei, token_decimals)}' if amount > max_repay_amount_wei else 'too small'}"
        logger.error(f"[{account._id}][{account.address_original}] Repay error: {error}")
