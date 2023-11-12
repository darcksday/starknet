import random

from loguru import logger
from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name
from helpers.starknet import Starknet
from modules.nft.config import FLEX_CONTRACT


def nft_flex(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Call Flex marketplace")

    call_data = random.randint(1, 20)
    flex_call = Call(
        to_addr=FLEX_CONTRACT,
        selector=get_selector_from_name("cancelMakerOrder"),
        calldata=[call_data],
    )

    transaction = account.sign_transaction([flex_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
