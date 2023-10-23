import time
from loguru import logger
from config.settings import *
from helpers.common import get_max_swap_amount_limited_dex
from modules.swaps.config import *


def get_min_amount_out(contract, amount: int, path: list):
    min_amount_out_data = contract.functions["get_amounts_out"].prepare(
        amountIn=amount,
        path=path
    ).call_sync()

    min_amount_out = min_amount_out_data.amounts
    return int(min_amount_out[1] - (min_amount_out[1] / 100 * SLIPPAGE_PCT))


def swap_token_jediswap(account, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using JediSwap")

    contract = account.get_contract(JEDISWAP_CONTRACT, JEDISWAP_ABI)

    get_max_swap_amount_limited_dex(from_token, amount)
    amount_wei = account.get_swap_amount(from_token, amount)
    path = [from_token, to_token]
    deadline = int(time.time()) + 1000000

    min_amount_out = get_min_amount_out(contract, amount_wei, path)

    # Approve
    approve_contract = account.get_contract(from_token)
    approve_call = approve_contract.functions["approve"].prepare(
        JEDISWAP_CONTRACT,
        amount_wei
    )

    # Swap
    swap_call = contract.functions["swap_exact_tokens_for_tokens"].prepare(
        amount_wei,
        min_amount_out,
        path,
        account.address,
        deadline
    )

    transaction = account.sign_transaction([approve_call, swap_call])
    transaction_response = account.send_transaction(transaction)

    return transaction_response.transaction_hash
