import time

import requests
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from termcolor import cprint

from common import TOKEN_ADDRESS
from config.settings import *
from config.settings import USE_REF
from helpers.common import get_random_proxy
from helpers.starknet import Starknet


def ocean_request(params, retry=0):
    proxies = get_random_proxy()
    url = "https://ethapi.openocean.finance/v1/starknet/swap-quote"

    response_req = requests.get(url=url, params=params, proxies=proxies)
    if response_req.status_code == 200:
        response = response_req.json()
        if 'transaction' in response and response['msg'] == 'ok':
            return response

    if retry < 5:
        cprint(f'Error: status code {response_req.status_code}, retry...', 'red')
        time.sleep(1)
        return ocean_request(params, retry + 1)
    else:
        raise Exception(f'SKIP. Response error')


def build_transaction(wallet_address: str, from_token: int, to_token: int, amount_wei: int):
    token_symbols = {v: k for k, v in TOKEN_ADDRESS.items()}
    fee_recipient = "0x00860d7dd27b165979a5a5c0b1ca44fb53a756ed80848613931dacb6a58ff5a0"

    params = {
        "inTokenSymbol": token_symbols.get(from_token),
        "inTokenAddress": hex(from_token),
        "outTokenSymbol": token_symbols.get(to_token),
        "outTokenAddress": hex(to_token),
        "amount": int(amount_wei),
        "gasPrice": 5000000000,
        "referrer": fee_recipient,
        "referrerFee": 0.001,
        "slippage": SLIPPAGE_PCT * 100,
        "account": wallet_address,
        "flags": 0,
    }

    # 0.003% fee
    if USE_REF:
        params.update({
            "referrer": fee_recipient,
            "referrerFee": 0.003
        })

    return ocean_request(params)


def swap_token_open_ocean(account: Starknet, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using OpenOcean")

    amount_wei = account.get_swap_amount(from_token, amount)
    if not amount_wei:
        return False

    response = build_transaction(account.address_original, from_token, to_token, amount_wei)

    calls_list = []
    for tx in response['transaction']:
        contract_integer = int(tx['contractAddress'], 16)
        data = []
        for i in tx['calldata']:
            if '0x' in str(i):
                data.append(int(i, 16))
            else:
                data.append(int(i))

        call = Call(
            to_addr=contract_integer,
            selector=get_selector_from_name(tx['entrypoint']),
            calldata=data,
        )
        calls_list.append(call)

    transaction = account.sign_transaction(calls_list)
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash
