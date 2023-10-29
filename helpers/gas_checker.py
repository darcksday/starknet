from starknet_py.net.gateway_client import GatewayClient
from config.settings import CHECK_GWEI, MAX_GWEI, MIN_SLEEP, MAX_SLEEP
from web3 import Web3
from loguru import logger

from helpers.cli import sleeping


def get_gas():
    try:
        client = GatewayClient("mainnet")
        block_data = client.get_block_sync("latest")
        gas = Web3.from_wei(block_data.gas_price, "gwei")
        return gas
    except Exception as error:
        logger.error(f'Read gas error: {str(error)}')


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
