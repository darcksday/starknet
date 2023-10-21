import random
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from common import TOKEN_ADDRESS
from modules.zklend.config import ZKLEND_CONCTRACTS


def zklend_collateral_enable(account, amount: float = 0, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: Enable Collateral")

    if not token:
        token = random.choice(list(TOKEN_ADDRESS.values()))

    enable_collateral_call = Call(
        to_addr=ZKLEND_CONCTRACTS["router"],
        selector=get_selector_from_name("enable_collateral"),
        calldata=[token],
    )

    transaction = account.sign_transaction([enable_collateral_call])
    transaction_response = account.send_transaction(transaction)

    return transaction_response.transaction_hash


def zklend_collateral_disable(account, amount=0, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: Disable Collateral")

    if not token:
        token = random.choice(list(TOKEN_ADDRESS.values()))

    disable_collateral_call = Call(
        to_addr=ZKLEND_CONCTRACTS["router"],
        selector=get_selector_from_name("disable_collateral"),
        calldata=[token],
    )

    transaction = account.sign_transaction([disable_collateral_call])
    transaction_response = account.send_transaction(transaction)

    return transaction_response.transaction_hash
