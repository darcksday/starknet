import random

from web3 import Web3

from common import RPC
from config.settings import CHECK_GWEI, MAX_GWEI, MIN_SLEEP, MAX_SLEEP
from loguru import logger

from helpers.cli import sleeping


def get_gas():
    try:
        w3 = Web3(Web3.HTTPProvider(random.choice(RPC["ethereum"]["rpc"])))
        gas_price = w3.eth.gas_price
        return w3.from_wei(gas_price, 'gwei')
    except Exception as error:
        logger.error(error)


def wait_gas():
    while True:
        gas = get_gas()

        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {"{:3.2f}".format(gas)} > {MAX_GWEI}, waiting...')
            sleeping(MIN_SLEEP, MAX_SLEEP)
        else:
            logger.success(f'GWEI is OK: {"{:3.2f}".format(gas)} < {MAX_GWEI}')
            break


def check_gas(func):
    def _wrapper(*args, **kwargs):
        if CHECK_GWEI:
            wait_gas()
        return func(*args, **kwargs)

    return _wrapper
