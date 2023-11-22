from loguru import logger
from helpers.starknet import Starknet
from modules.nft.config import GOL2_CONTRACT, GOL2_ABI


def nft_gol2(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Mint GoL2 token")

    contract = account.get_contract(GOL2_CONTRACT, GOL2_ABI)
    mint_call = contract.functions["evolve"].prepare(39132555273291485155644251043342963441664)

    transaction = account.sign_transaction([mint_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
