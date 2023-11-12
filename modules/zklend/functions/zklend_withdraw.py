from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from common import TOKEN_ADDRESS
from helpers.common import int_to_wei
from modules.zklend.common import get_deposit_amount
from modules.zklend.config import ZKLEND_CONCTRACTS


def zklend_withdraw(account, amount: float, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: ZkLend Withdraw")

    if not token:
        token = TOKEN_ADDRESS["ETH"]

    balance_wei = get_deposit_amount(account, token)
    if not amount:
        amount = balance_wei
    elif int_to_wei(amount) >= balance_wei:
        amount = int_to_wei(amount)
    else:
        raise ValueError("Wrong amount, leave empty for all balance")

    if amount > 0:
        withdraw_all_call = Call(
            to_addr=ZKLEND_CONCTRACTS["router"],
            selector=get_selector_from_name("withdraw_all"),
            calldata=[token],
        )

        transaction = account.sign_transaction([withdraw_all_call])
        transaction_response = account.send_transaction(transaction)
        if transaction_response:
            return transaction_response.transaction_hash
    else:
        logger.error(f"[{account._id}][{account.address_original}] Deposit not found")
