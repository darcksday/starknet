import random
from loguru import logger
from common import TOKEN_ADDRESS
from helpers.starknet import Starknet
from modules.nft.config import PYRAMID_CONTRACT, PYRAMID_ABI


def get_mint_cost(contract):
    fee = contract.functions["returnMintCost"].call_sync(block_number="latest")
    return fee.cost


def nft_pyramid(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Mint NFT using Pyramid")

    contract = account.get_contract(PYRAMID_CONTRACT, PYRAMID_ABI)
    mint_id = random.randint(11111111111111111111, 999999999999999999999)
    fee_cost = get_mint_cost(contract)

    approve_contract = account.get_contract(TOKEN_ADDRESS["ETH"])
    approve_call = approve_contract.functions["approve"].prepare(
        PYRAMID_CONTRACT,
        fee_cost
    )
    mint_call = contract.functions["mint"].prepare(
        mint_id
    )

    transaction = account.sign_transaction([approve_call, mint_call])
    transaction_response = account.send_transaction(transaction)

    return transaction_response.transaction_hash
