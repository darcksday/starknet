import random
from loguru import logger
from helpers.starknet import Starknet
from modules.nft.config import UNFRAMED_CONTRACT, UNFRAMED_ABI


def nft_unframed(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Call Unframed marketplace (cheap tx)")

    random_nonce = random.randint(
        296313738189912513306030367211954909183182558840765666364410788857347237284,
        3618502788666131213697322783095070105623107215331596699973092056135872020480
    )

    contract = account.get_contract(UNFRAMED_CONTRACT, UNFRAMED_ABI, 1)
    unframed_call = contract.functions["cancel_orders"].prepare(order_nonces=[random_nonce])

    transaction = account.sign_transaction([unframed_call], 1)
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
