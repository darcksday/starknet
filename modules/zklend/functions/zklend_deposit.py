from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from common import TOKEN_ADDRESS
from modules.zklend.config import ZKLEND_CONCTRACTS


def zklend_deposit(account, amount: float, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: ZkLend Deposit")

    if not token:
        token = TOKEN_ADDRESS["ETH"]

    approve_contract = account.get_contract(token)
    amount_wei = account.get_swap_amount(token, amount)

    approve_call = approve_contract.functions["approve"].prepare(
        ZKLEND_CONCTRACTS["router"],
        amount_wei
    )

    deposit_call = Call(
        to_addr=ZKLEND_CONCTRACTS["router"],
        selector=get_selector_from_name("deposit"),
        calldata=[token, amount_wei],
    )

    transaction = account.sign_transaction([approve_call, deposit_call])
    transaction_response = account.send_transaction(transaction)

    return transaction_response.transaction_hash
