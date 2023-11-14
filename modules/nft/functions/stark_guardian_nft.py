import random
from loguru import logger

from helpers.starknet import Starknet
from modules.nft.config import STARKGUARDIANS_ABI, STARKGUARDIANS_CONTRACT


def get_random_name_symbol():
    token_name = "".join(random.sample([chr(i) for i in range(95, 120)], random.randint(6, 14)))
    token_symbol = token_name.upper()[0:random.randint(3, 4)]
    return token_name, token_symbol


def nft_deploy_stark_guardian(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Deploy NFT to starkGuardians (1/2)")

    contract = account.get_contract(STARKGUARDIANS_CONTRACT, STARKGUARDIANS_ABI)

    token_name, token_symbol = get_random_name_symbol()
    deploy_call = contract.functions["deployContract"].prepare(
        0x745c9a10e7bc32095554c895490cfaac6c4c8cada2e3763faddedfaa72c856a,
        random.randint(38890058876971531151, 85735143683896744799),
        1,
        [
            token_name,
            token_symbol,
            account.address_original,
        ]
    )

    transaction = account.sign_transaction([deploy_call])
    transaction_response = account.send_transaction(transaction)

    if transaction_response:
        logger.info(f"[{account._id}][{account.address_original}] Mint starkGuardians NFT (2/2)")
        account.wait_until_tx_finished(transaction_response.transaction_hash)

        tx_data = account.get_transaction(transaction_response.transaction_hash)
        print('tx_data', tx_data)

        contract = account.get_contract(tx_data.events[0].from_address, STARKGUARDIANS_ABI)

        mint_call = contract.functions["mint"].prepare(account.address_original)
        transaction2 = account.sign_transaction([mint_call])
        transaction2_response = account.send_transaction(transaction2)

        if transaction2_response:
            return transaction2_response.transaction_hash
