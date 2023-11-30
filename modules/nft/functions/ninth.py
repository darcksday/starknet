from loguru import logger
from helpers.starknet import Starknet
from modules.nft.config import NINTH_ABI, NINTH_CONTRACT


def nft_ninth(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] The Ninth approve")

    contract = account.get_contract(NINTH_CONTRACT, NINTH_ABI, cairo_version=1)
    approve_call = contract.functions["approve"].prepare(
        0x274a2ef0e6aadb781777954ec78832fbe490de0f0f1484354b99f328f74ab36,
        20
    )

    transaction = account.sign_transaction([approve_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
