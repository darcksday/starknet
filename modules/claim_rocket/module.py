import random

from hashlib import sha256
from loguru import logger
import requests

from helpers.common import get_random_proxy
from helpers.starknet import Starknet
from modules.claim_rocket.config import CLAIM_CONTRACT, ROCKER_ABI


def rocket_claim(account: Starknet,amount=0):
    logger.info(f"[{account._id}][{account.address_original}] Claim Rocket")



    points =get_points(account.address_original)
    print(points)
    proof =get_proof(account.address_original)
    integers = [int(hex_str, 16) for hex_str in proof]

    referer=0x678f58f34094e3b8deef86fd6085f55a3a4563bed7c18159d7bbfb3a7cce87a
    rocket_contract = account.get_contract(CLAIM_CONTRACT, ROCKER_ABI,1)
    claim_call = rocket_contract.functions["claim"].prepare(
        points,
        integers,
        int(referer)
    )



    transaction = account.sign_transaction([claim_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash


def get_points(address):
    url = "https://starkrocket.xyz/api/check_wallet"

    params = {
        "address": address,
    }


    proxies = get_random_proxy()
    response = requests.get(url, params=params, proxies=proxies)
    response_data = response.json()

    if 'points' in response_data['result']:
        return response_data['result']['points']


def get_proof(address):
    url = "https://starkrocket.xyz/api/get_proof"

    params = {
        "address": address,
    }

    # if USE_REF:
    #     params['integratorFees'] = hex(3)
    #     params['integratorFeeRecipient'] = fees

    proxies = get_random_proxy()
    response = requests.get(url, params=params, proxies=proxies)
    response_data = response.json()
    if 'proof' in response_data['result']:
        return response_data['result']['proof']