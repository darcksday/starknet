from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

from helpers.starknet import Starknet
from modules.nft.config import STARKVERSE_CONTRACT


def nft_starkverse(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Mint NFT using StarkVerse")

    mint_starknet_id_call = Call(
        to_addr=STARKVERSE_CONTRACT,
        selector=get_selector_from_name("publicMint"),
        calldata=[account.address],
    )

    transaction = account.sign_transaction([mint_starknet_id_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
