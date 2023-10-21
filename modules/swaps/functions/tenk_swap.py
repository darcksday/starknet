import time
from loguru import logger
from config.settings import *
from modules.swaps.config import STARKSWAP_CONTRACT, STARKSWAP_ABI


def get_min_amount_out(contract, amount: int, slippage: float, path: list):
    min_amount_out_data = contract.functions["getAmountsOut"].prepare(
        amountIn=amount,
        path=path
    ).call_sync()

    min_amount_out = min_amount_out_data.amounts
    return int(min_amount_out[1] - (min_amount_out[1] / 100 * slippage))


def swap_token_10kswap(account, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using 10kSwap")

    path = [from_token, to_token]
    deadline = int(time.time()) + 1000000
    amount_wei = account.get_swap_amount(from_token, amount)

    contract = account.get_contract(STARKSWAP_CONTRACT, STARKSWAP_ABI)
    min_amount_out = get_min_amount_out(contract, amount_wei, SLIPPAGE_PCT, path)

    approve_contract = account.get_contract(from_token)
    approve_call = approve_contract.functions["approve"].prepare(
        STARKSWAP_CONTRACT,
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

    return transaction_response.transaction_hash
