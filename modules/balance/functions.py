import time
from loguru import logger
from common import TOKEN_ADDRESS
from helpers.starknet import Starknet


def one_wallet_balance(account: Starknet, contract_address=None):
    try:
        if contract_address == TOKEN_ADDRESS["ETH"]:
            balance_wei = account.get_eth_balance()
            balance = "{:8.6f}".format(balance_wei / 10 ** 18)
            symbol = "ETH"
        else:
            token = account.get_balance(contract_address)
            balance = "{:8.6f}".format(token["balance_wei"] / 10 ** 18)
            symbol = token["symbol"]

        logger.info(f"[{account._id}][{account.address_original}]: {balance} {symbol}")
        return balance

    except Exception:
        time.sleep(1)
        return one_wallet_balance(account, contract_address)
