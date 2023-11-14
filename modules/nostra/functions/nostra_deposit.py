from loguru import logger
from common import TOKEN_ADDRESS
from helpers.common import wei_to_int
from helpers.starknet import Starknet
from modules.nostra.config import NOSTRA_CONTRACTS, NOSTRA_ABI, NOSTRA_DEPOSIT_LIMITS


def nostra_deposit(account: Starknet, amount: float, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: Nostra Deposit")

    if not token:
        token = TOKEN_ADDRESS["ETH"]
    token_symbols = {v: k for k, v in TOKEN_ADDRESS.items()}
    token_symbol = token_symbols[token]

    approve_contract = account.get_contract(token)
    amount_wei = account.get_swap_amount(token, amount)
    if not amount_wei:
        logger.error(f"[{account._id}][{account.address_original}] Not enough token balance")
        return False

    if amount_wei > NOSTRA_DEPOSIT_LIMITS[token_symbol]:
        token_decimals = account.get_balance(token)["decimal"]
        info_amount = wei_to_int(NOSTRA_DEPOSIT_LIMITS[token_symbol], token_decimals)
        logger.info(f"[{account._id}][{account.address_original}] Nostra limit: {info_amount} {token_symbol}, we will use this amount")
        amount_wei = NOSTRA_DEPOSIT_LIMITS[token_symbol]

    approve_call = approve_contract.functions["approve"].prepare(
        NOSTRA_CONTRACTS[token_symbol],
        amount_wei
    )

    nostra_contract = account.get_contract(NOSTRA_CONTRACTS[token_symbol], NOSTRA_ABI)
    deposit_call = nostra_contract.functions["mint"].prepare(
        account.address,
        amount_wei
    )

    transaction = account.sign_transaction([approve_call, deposit_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
