import sys
import random
import time
import traceback

from loguru import logger
from common import TOKEN_ADDRESS
from config.settings import *
from datetime import datetime
from helpers.common import wait_schedule, get_private_keys
from helpers.gas_checker import check_gas
from helpers.starknet import Starknet
from helpers.cli import get_amount_in_range, sleeping
from helpers.csv_helper import start_csv, write_csv_error, write_csv_success
from modules.orbiter_bridge.functions import orbiter_bridge_to_starknet
from modules.swaps.swap_routes import SWAP_ROUTES


@check_gas
def call_function(
        account: Starknet,
        method,
        _amount: str,
        params: list = [],
        csv: str = '',
        retry: int = 0
):
    amount = get_amount_in_range(_amount)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    csv_name = method.__name__

    if csv != '':
        csv_name = csv

    try:
        tx_hash = method(account, amount, *params)
        if tx_hash and method not in [orbiter_bridge_to_starknet]:
            # account.wait_until_tx_finished(tx_hash)
            write_csv_success(account._id, {
                'status': 1,
                'csv_name': csv_name,
                'function': method.__name__,
                'date': formatted_datetime,
            })
        return True

    except Exception as error:
        # print(str(error), 'call_function error, retry...')
        exc_type, exc_value, exc_traceback = sys.exc_info()

        traceback_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
        full_track_error = "".join(traceback_details)
        logger.error(full_track_error)

        write_csv_error(csv_name, [
            account.address_original,
            account.private_key,
            method.__name__,
            params,
            full_track_error,
            formatted_datetime
        ])

        if ('Insufficient max fee' in str(error) or 'Server Error' in str(error)) and retry < 5:
            time.sleep(10)
            return call_function(account, method, _amount, params, csv, retry + 1)
        else:
            logger.error(f'[{account._id}][{account.address_original}]: {error}')


def run_script(method, _amount: str, params=[], specific_prt={}):
    if SCHEDULE_TIME:
        wait_schedule(SCHEDULE_TIME)

    csv_name = method.__name__
    start_csv(csv_name)
    prt_keys = [specific_prt] if specific_prt else get_private_keys()

    for _id, wallet in enumerate(prt_keys):
        account = Starknet(wallet['index'], wallet)
        call_function(
            account,
            method,
            _amount,
            params
        )

        if _id < len(prt_keys) - 1:
            sleeping(MIN_SLEEP, MAX_SLEEP)


def run_random_function(functions: list, _amount: str = 0):
    prt_keys = get_private_keys()
    for _id, wallet in enumerate(prt_keys):
        account = Starknet(wallet['index'], wallet)
        random_func = random.choice(functions)
        run_script_one(account, random_func, "0", [], random_func.__name__)

        if _id < len(prt_keys) - 1:
            sleeping(MIN_SLEEP, MAX_SLEEP)


def run_random_swap(routes: dict, _amount: str, specific_prt=None):
    if SCHEDULE_TIME:
        wait_schedule(SCHEDULE_TIME)

    csv_name_1 = 'random_swap_1'
    csv_name_2 = 'random_swap_2'
    start_csv(csv_name_1)
    start_csv(csv_name_2)

    prt_keys = [specific_prt] if specific_prt else get_private_keys()

    for _id, wallet in enumerate(prt_keys):
        account = Starknet(wallet['index'], wallet)
        run_random_swap_one(account, routes, _amount, csv_name_1, csv_name_2)

        if _id < len(prt_keys) - 1:
            sleeping(MIN_SLEEP, MAX_SLEEP)


def run_multiple(functions: list):
    prt_keys = get_private_keys()
    wallets_paths = {}
    fn_len = len(sort_functions(functions))

    for fn_index in range(fn_len):
        for _id, item in enumerate(prt_keys):
            path = generate_path(item, wallets_paths, functions)
            function = path[fn_index]
            logger.info(f'Step {fn_index + 1}/{fn_len} - {function.__name__}')

            if function.__name__ == 'run_random_swap':
                run_random_swap(SWAP_ROUTES, '', item)
            else:
                run_script(function, '', [], item)

            if _id < len(prt_keys) - 1:
                sleeping(MIN_SLEEP, MAX_SLEEP)


def run_one_of_multiple(_functions: list):
    prt_keys = get_private_keys()
    wallets_paths = {}

    for _id, item in enumerate(prt_keys):
        functions = [random.choice(_functions)]
        fn_len = len(sort_functions(functions))
        path = generate_path(item, wallets_paths, functions)

        for fn_index in range(fn_len):
            function = path[fn_index]
            logger.info(f'Step {fn_index + 1}/{fn_len} - {function.__name__}')

            if function.__name__ == 'run_random_swap':
                run_random_swap(SWAP_ROUTES, '', item)
            else:
                run_script(function, '', [], item)

            if _id < len(prt_keys) - 1:
                sleeping(MIN_SLEEP, MAX_SLEEP)


def generate_path(item, wallets_paths, functions):
    if not item['index'] in wallets_paths:
        random.shuffle(functions)
        sorted_functions = sort_functions(functions)
        wallets_paths[item['index']] = sorted_functions

    path = wallets_paths[item['index']]
    # route_string = ", ".join(function.__name__ for function in path)
    # cprint(f' Full Route: {route_string}', "yellow")

    return path


def sort_functions(functions):
    sorted_functions = []
    for function in functions:
        if isinstance(function, list):
            sorted_functions.extend(function)
        else:
            sorted_functions.append(function)
    return sorted_functions


def run_script_one(account: Starknet, method, _amount: str, params=[], csv_name=''):
    start_csv(csv_name)

    call_function(
        account,
        method,
        _amount,
        params,
        csv_name
    )


def run_random_swap_one(account: Starknet, routes, _amount: str, csv_name_1, csv_name_2):
    random_dex = random.choice(list(routes.items()))
    random_dex = random_dex[1]
    random_token = random.choice(list(random_dex['tokens']))
    method = random_dex['function']

    additional_params = []
    if 'params' in random_dex:
        additional_params = random_dex['params']

    params = additional_params + [TOKEN_ADDRESS['ETH'], random_token]
    reverted_params = additional_params + [random_token, TOKEN_ADDRESS['ETH']]

    logger.info(f'Step 1: Sell ETH')
    step1_success = call_function(
        account,
        method,
        _amount,
        params,
        csv_name_1
    )

    if step1_success:
        sleeping(MIN_SLEEP, MAX_SLEEP)
        logger.info(f'Step 2: Buy Back ETH')

        call_function(
            account,
            method,
            "0",
            reverted_params,
            csv_name_2
        )
