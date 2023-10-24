import random

from hashlib import sha256
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from helpers.starknet import Starknet
from modules.dmail.config import DMAIL_CONTRACT


def dmail_send_email(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Dmail: Send random email")

    email_address = sha256(str(1e10 * random.random()).encode()).hexdigest()
    theme = sha256(str(1e10 * random.random()).encode()).hexdigest()

    dmail_call = Call(
        to_addr=DMAIL_CONTRACT,
        selector=get_selector_from_name("transaction"),
        calldata=[
            email_address[0:31],
            theme[0:31]
        ],
    )

    transaction = account.sign_transaction([dmail_call])
    transaction_response = account.send_transaction(transaction)

    return transaction_response.transaction_hash
