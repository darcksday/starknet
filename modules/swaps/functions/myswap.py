from loguru import logger
from common import TOKEN_ADDRESS
from config.settings import *
from helpers.common import get_max_swap_amount_limited_dex
from helpers.starknet import Starknet
from modules.swaps.config import MYSWAP_POOLS, MYSWAP_CONTRACT, MYSWAP_ABI

# Get mySwap pool ID
def get_pool_id(from_token: str, to_token: str):
    reverse = False

    pool_id = MYSWAP_POOLS.get(from_token + to_token)
    if pool_id is None:
        reverse = True
        pool_id = MYSWAP_POOLS.get(to_token + from_token)
        if pool_id is None:
            logger.error(f"Pool {from_token} <-> {to_token} not found")
            return
    return pool_id, reverse

# Get min amount out
def get_min_amount_out(contract, pool_id: int, reverse: bool, amount: int, slippage: float):
    (pool_data,) = contract.functions["get_pool"].prepare(
        pool_id
    ).call_sync()

    if reverse:
        reserve_in = pool_data.get("token_b_reserves")
        reserve_out = pool_data.get("token_a_reserves")
    else:
        reserve_in = pool_data.get("token_a_reserves")
        reserve_out = pool_data.get("token_b_reserves")

    min_amount_out = reserve_out * amount / reserve_in
    return int(min_amount_out - (min_amount_out / 100 * slippage))


def swap_token_myswap(account: Starknet, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using MySwap")

    contract = account.get_contract(MYSWAP_CONTRACT, MYSWAP_ABI)

    token_symbols = {v: k for k, v in TOKEN_ADDRESS.items()}
    from_token_symbol = token_symbols.get(from_token)
    if not from_token_symbol:
        raise Exception(f'Token not found: {from_token}')

    to_token_symbol = token_symbols.get(to_token)
    if not from_token_symbol:
        raise Exception(f'Token not found: {to_token}')

    get_max_swap_amount_limited_dex(from_token, amount)

    amount_wei = account.get_swap_amount(from_token, amount)
    if not amount_wei:
        return False

    pool_id, reverse = get_pool_id(from_token_symbol, to_token_symbol)
    min_amount_out = get_min_amount_out(contract, pool_id, reverse, amount_wei, SLIPPAGE_PCT)

    approve_contract = account.get_contract(from_token)
    approve_call = approve_contract.functions["approve"].prepare(
        MYSWAP_CONTRACT,
        amount_wei
    )

    swap_call = contract.functions["swap"].prepare(
        pool_id,
        from_token,
        amount_wei,
        min_amount_out,
    )

    transaction = account.sign_transaction([approve_call, swap_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
