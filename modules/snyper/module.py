import asyncio
from datetime import datetime
import time

from loguru import logger
from starknet_py.net.models import StarknetChainId

from common import ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW
from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping, print_input_contract_address, print_input_amounts_range
from helpers.common import get_private_keys
from helpers.csv_helper import write_csv_error, write_csv_success, start_csv
from helpers.factory import run_script, run_script_one
from helpers.gas_checker import check_gas
from helpers.starknet import Starknet
from modules.swaps.functions.avnu import swap_token_avnu


def interface_snyper():
    from_token = print_input_contract_address("From token / address or symbol")
    to_token = print_input_contract_address("To token / address or symbol")
    amount_str = print_input_amounts_range('Swap amount')
    params = [from_token, to_token]

    # chose swap function
    # run_script(swap_token_avnu, amount_str, params)

    logger.info("Deploy new argent wallets")

    wallet_list = get_private_keys()
    wallet = wallet_list[0]
    account = Starknet(wallet["index"], wallet)

    # for _id, wallet in enumerate(wallet_list):
    #     if not account.address_original:
    #         logger.error(f'Error: No wallet address provided')
    #         continue
    #     break

    try:

        block = account.client.get_block_number_sync()
        logger.info(f'Latest accepted block: {block}')

        # asyncio.run(bla(account))

        while True:

            check_block = account.client.get_block_number_sync() + 1
            if check_block != block:
                logger.info(f'New block found: {check_block}')
                block = check_block

                logger.info(f'Try to swap:')
                # asyncio.run(send_tokens(web3_async, private_keys))
                # print(123)

                run_script_one(account, swap_token_avnu, amount_str, params)

            time.sleep(0.5)


    except Exception as e:
        logger.error(f'Error: {e}')
