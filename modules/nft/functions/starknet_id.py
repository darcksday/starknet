import random
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from helpers.starknet import Starknet
from modules.nft.config import STARKNET_ID_CONTRACT


def nft_starknet_id(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Mint NFT using StarkNet ID")

    mint_starknet_id_call = Call(
        to_addr=STARKNET_ID_CONTRACT,
        selector=get_selector_from_name("mint"),
        calldata=[int(random.random() * 1e12)],
    )

    transaction = account.sign_transaction([mint_starknet_id_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
