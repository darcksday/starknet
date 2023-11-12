import random
from loguru import logger

from common import TOKEN_ADDRESS
from helpers.common import int_to_wei
from helpers.starknet import Starknet
from modules.nft.config import STARK_STARS_CONTRACTS, STARKSTARS_ABI


def nft_starkstars(account: Starknet, amount=0):
    approve_contract = account.get_contract(TOKEN_ADDRESS["ETH"])
    stark_star_address = random.choice(STARK_STARS_CONTRACTS)

    nft_contract = account.get_contract(stark_star_address, STARKSTARS_ABI, 1)
    logger.info(f"[{account._id}][{account.address_original}] Mint StarkStars NFT")

    approve_call = approve_contract.functions["approve"].prepare(
        stark_star_address,
        int_to_wei(0.0001)
    )

    mint_starkstars_call = nft_contract.functions["mint"].prepare()

    transaction = account.sign_transaction([approve_call, mint_starkstars_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
