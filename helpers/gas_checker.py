import random

from common import RPC
from config.settings import *
from web3 import Web3
from loguru import logger

from helpers.cli import sleeping
from helpers.retry import retry
from starknet_py.net.full_node_client import FullNodeClient


@retry
def get_gas():
    if not CUSTOM_RPC:
        client = FullNodeClient(random.choice(RPC["starknet"]["rpc"]))
    else:
        client = FullNodeClient(CUSTOM_RPC)
    block_data = client.get_block_sync("latest")
    gas = Web3.from_wei(block_data.gas_price, "gwei")
    return gas


def wait_gas():
    while True:
        gas = get_gas()

        if gas and gas > MAX_GWEI:
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
