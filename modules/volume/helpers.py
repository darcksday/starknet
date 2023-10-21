import time
import ccxt

from dotenv import dotenv_values
from loguru import logger
from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import int_to_wei
from helpers.starknet import Starknet
from modules.exchange_withdraw.config import CEX_KEYS

config = dotenv_values("config/.env")


def check_wait_wallet_balance(account: Starknet, amount, token_symbol, contract_address=None):
    while True:
        logger.info(f"[{account._id}][{account.address_original}] Check wallet Balance: wait at least {amount} {token_symbol}")

        if contract_address is None:
            balance_wei = account.account.get_balance_sync()
            token_decimals = 18
        else:
            token = account.get_balance(contract_address)
            balance_wei = token['balance_wei']
            token_decimals = account.get_balance(contract_address)["decimal"]

        balance = "{:4.4f}".format(balance_wei / 10 ** token_decimals)
        if balance_wei >= int_to_wei(amount, token_decimals):
            logger.info(f"[{account._id}][{account.address_original}] {balance} {token_symbol} found")
            time.sleep(5)
            return balance

        sleeping(MIN_SLEEP, MAX_SLEEP)
        continue


def get_okx_account(sub_account=0):
    conf = CEX_KEYS[f'okx-sub-{sub_account}'] if sub_account else CEX_KEYS['okx']

    return ccxt.okx({
        'apiKey': conf['api_key'],
        'secret': conf['api_secret'],
        'password': conf['password'],
        'enableRateLimit': True,
        'options': {
            'defaultType': 'main',
        }
    })


def get_okx_token_balance(sub_account=0, token='ETH'):
    okx_main_account = get_okx_account(sub_account)
    balances = okx_main_account.fetch_balance({"ccy": token, "type": "funding"})
    return balances['free'][token]
