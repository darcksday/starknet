import time
from loguru import logger
from config.settings import *
from helpers.common import get_max_swap_amount_limited_dex
from helpers.starknet import Starknet
from modules.swaps.config import PROTOSS_CONTRACT, PROTOSS_ABI


def get_min_amount_out(contract, amount: int, slippage: float, path: list):
    min_amount_out_data = contract.functions["getAmountsOut"].prepare(
        amountIn=amount,
        path=path
    ).call_sync()

    min_amount_out = min_amount_out_data.amounts
    return int(min_amount_out[1] - (min_amount_out[1] / 100 * slippage))


def swap_token_protoss(account: Starknet, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using Protoss")

    amount_wei = account.get_swap_amount(from_token, amount)
    if not amount_wei:
        return False

    contract = account.get_contract(PROTOSS_CONTRACT, PROTOSS_ABI)
    get_max_swap_amount_limited_dex(from_token, amount)

    path = [from_token, to_token]
    deadline = int(time.time()) + 1000000
    min_amount_out = get_min_amount_out(contract, amount_wei, SLIPPAGE_PCT, path)

    approve_contract = account.get_contract(from_token)
    approve_call = approve_contract.functions["approve"].prepare(
        PROTOSS_CONTRACT,
        amount_wei
    )

    swap_call = contract.functions["swapExactTokensForTokens"].prepare(
        amount_wei,
        min_amount_out,
        path,
        account.address,
        deadline
    )

    transaction = account.sign_transaction([approve_call, swap_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
