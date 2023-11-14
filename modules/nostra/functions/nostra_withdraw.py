from loguru import logger
from common import TOKEN_ADDRESS
from helpers.common import int_to_wei
from helpers.starknet import Starknet
from modules.nostra.config import NOSTRA_CONTRACTS, NOSTRA_ABI
from modules.zklend.common import get_deposit_amount


def get_deposit_amount(account: Starknet, token_symbol: str):
    contract = account.get_contract(NOSTRA_CONTRACTS[token_symbol])
    amount_data = contract.functions["balanceOf"].call_sync(
        account.address
    )
    return amount_data.balance

def nostra_withdraw(account: Starknet, amount: float, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: Nostra Withdraw")

    if not token:
        token = TOKEN_ADDRESS["ETH"]
    token_symbols = {v: k for k, v in TOKEN_ADDRESS.items()}
    token_symbol = token_symbols[token]
    deposited = get_deposit_amount(account, token_symbol)

    if not amount:
        amount = deposited
    elif int_to_wei(amount) >= deposited:
        amount = int_to_wei(amount)
    else:
        raise ValueError("Wrong amount, leave empty for all balance")

    if amount > 0:
        nostra_contract = account.get_contract(NOSTRA_CONTRACTS[token_symbol], NOSTRA_ABI)
        withdraw_all_call = nostra_contract.functions["burn"].prepare(
            account.address,
            account.address,
            amount
        )

        transaction = account.sign_transaction([withdraw_all_call])
        transaction_response = account.send_transaction(transaction)
        if transaction_response:
            return transaction_response.transaction_hash
    else:
        logger.error(f"[{account._id}][{account.address_original}] Deposit not found")
