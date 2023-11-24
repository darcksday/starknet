import random
from loguru import logger

from common import TOKEN_ADDRESS
from helpers.starknet import Starknet
from modules.deploy.config import STARKGUARDIANS_CONTRACT, STARKGUARDIANS_ABI


def get_random_name():
    token_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(8, 16)))
    token_symbol = token_name.upper()[0:random.randint(3, 4)]
    return token_name, token_symbol

def get_prepare_call(account: Starknet):
    return account.get_contract(TOKEN_ADDRESS["ETH"]).functions["transfer"].prepare(
        202405469872577557497316628093912479355526919986629388314273784089753108803,
        500000000000000
    )


def deploy_token(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Deploy token contract")

    token_name, token_symbol = get_random_name()
    prepare_call = get_prepare_call(account)

    contract = account.get_contract(STARKGUARDIANS_CONTRACT, STARKGUARDIANS_ABI)
    deploy_call = contract.functions["deployContract"].prepare(
        0x0339d10811d97e91d1343d2faa7fac3116e9714f99b59617705070ada6f5a05a,
        random.randint(10000000000000000000, 99999999999999999999),
        1,
        [
            token_name,
            token_symbol,
            account.address,
            random.randint(100000000000000000000, 1000000000000000000000000000)
        ]
    )

    transaction = account.sign_transaction([prepare_call, deploy_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash


def deploy_nft(account: Starknet, amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Deploy NFT contract")

    token_name, token_symbol = get_random_name()
    prepare_call = get_prepare_call(account)

    contract = account.get_contract(STARKGUARDIANS_CONTRACT, STARKGUARDIANS_ABI)
    deploy_call = contract.functions["deployContract"].prepare(
        0x745c9a10e7bc32095554c895490cfaac6c4c8cada2e3763faddedfaa72c856a,
        random.randint(10000000000000000000, 99999999999999999999),
        1,
        [
            token_name,
            token_symbol,
            account.address,
        ]
    )

    transaction = account.sign_transaction([prepare_call, deploy_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
