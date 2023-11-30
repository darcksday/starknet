from loguru import logger
from helpers.starknet import Starknet
from modules.nft.config import ALMANAC_ABI, ALMANAC_CONTRACT


def nft_almanac(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Almanac approve")

    contract = account.get_contract(ALMANAC_CONTRACT, ALMANAC_ABI)
    approve_call = contract.functions["setApprovalForAll"].prepare(
        0x7d4dc2bf13ede97b9e458dc401d4ff6dd386a02049de879ebe637af8299f91d,
        1
    )

    transaction = account.sign_transaction([approve_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
