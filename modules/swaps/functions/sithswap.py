import time
from loguru import logger
from config.settings import *
from helpers.starknet import Starknet
from modules.swaps.config import SITHSWAP_CONTRACT, SITHSWAP_ABI

# Get min amount out
def get_min_amount_out(contract, amount: int, slippage: float, path: list):
    min_amount_out_data = contract.functions["getAmountOut"].prepare(
        amount,
        path[0],
        path[1]
    ).call_sync()

    min_amount_out = min_amount_out_data.amount
    stable = min_amount_out_data.stable
    return int(min_amount_out - (min_amount_out / 100 * slippage)), stable


def swap_token_sithswap(account: Starknet, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using SithSwap")

    amount_wei = account.get_swap_amount(from_token, amount)
    if not amount_wei:
        return False

    contract = account.get_contract(SITHSWAP_CONTRACT, SITHSWAP_ABI)

    path = [from_token, to_token]
    deadline = int(time.time()) + 1000000
    min_amount_out, stable = get_min_amount_out(contract, amount_wei, SLIPPAGE_PCT, path)
    route = [{"from_address": path[0], "to_address": path[1], "stable": stable}]

    approve_contract = account.get_contract(from_token)
    approve_call = approve_contract.functions["approve"].prepare(
        SITHSWAP_CONTRACT,
        amount_wei
    )

    swap_call = contract.functions["swapExactTokensForTokensSupportingFeeOnTransferTokens"].prepare(
        amount_wei,
        min_amount_out,
        route,
        account.address,
        deadline
    )

    transaction = account.sign_transaction([approve_call, swap_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
