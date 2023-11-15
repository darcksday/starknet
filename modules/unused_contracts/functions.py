import random

import requests
import json

from loguru import logger

from helpers.cli import sleeping
from helpers.common import get_random_proxy
from helpers.csv_helper import start_csv
from helpers.factory import run_script, run_script_one, run_random_swap, run_random_swap_one
from helpers.retry import retry
from helpers.starknet import Starknet
from modules.swaps.swap_routes import SWAP_ROUTES
from modules.unused_contracts.config import ALL_CONTRACT_FUNCTIONS


def get_node_contract(contracts: set, edges):
    for edge in edges:
        if edge.get('node').get('main_calls'):
            for main_call in edge['node']['main_calls']:
                contracts.add(main_call['contract_address'].replace('0x0', '0x'))
    return contracts


@retry
def send_graphql_request(address, cursor):
    url = "https://api.starkscancdn.com/graphql"
    body = """query TransactionsTableQuery(\n  $first: Int!\n  $after: String\n  $input: TransactionsInput!\n) {\n  ...TransactionsTablePaginationFragment_transactions_2DAjA4\n}\n\nfragment TransactionsTableExpandedItemFragment_transaction on Transaction {\n  entry_point_selector_name\n  calldata_decoded\n  entry_point_selector\n  calldata\n  initiator_address\n  initiator_identifier\n  main_calls {\n    selector\n    selector_name\n    calldata_decoded\n    selector_identifier\n    calldata\n    contract_address\n    contract_identifier\n    id\n  }\n}\n\nfragment TransactionsTablePaginationFragment_transactions_2DAjA4 on Query {\n  transactions(first: $first, after: $after, input: $input) {\n    edges {\n      node {\n        id\n        ...TransactionsTableRowFragment_transaction\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment TransactionsTableRowFragment_transaction on Transaction {\n  id\n  transaction_hash\n  block_number\n  transaction_status\n  transaction_type\n  timestamp\n  initiator_address\n  initiator_identifier\n  initiator {\n    is_social_verified\n    id\n  }\n  main_calls {\n    selector_identifier\n    id\n  }\n  ...TransactionsTableExpandedItemFragment_transaction\n}\n"""
    variables = {
        "first": 30,
        "after": cursor,
        "input": {
            "initiator_address": str(address),
            "transaction_types": None,
            "sort_by": "timestamp",
            "order_by": "desc",
            "min_block_number": None,
            "max_block_number": None,
            "min_timestamp": None,
            "max_timestamp": None
        }
    }

    rand_version = random.randint(114, 118)
    macos_version = random.randint(5, 7)

    headers = {
        "Content-Type": "application/json",
        "Dnt": "1",
        "Origin": "https://starkscan.co",
        "Referer": "https://starkscan.co/",
        "Sec-Ch-Ua": f'"Chromium";v="{rand_version}", "Google Chrome";v="{rand_version}", "Not=A?Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_{macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{rand_version}.0.0.0 Safari/537.36"
    }

    proxies = get_random_proxy()
    response = requests.post(url, json={
        "query": body,
        "variables": variables
    }, headers=headers, proxies=proxies, timeout=40)
    if response.status_code == 200:
        my_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data.get('data') and data['data'].get('transactions'):
            transactions = data['data'].get('transactions')
            return transactions['pageInfo'].get('endCursor'), transactions.get('edges')
    else:
        logger.error('Request Error, response.status_code: ', response.status_code)


def get_used_contracts_list(address):
    contracts = set()
    cursor = None

    while True:
        cursor, edges = send_graphql_request(address, cursor)
        if edges:
            contracts = get_node_contract(contracts, edges)
        if not cursor:
            break

    return contracts


def run_random_unused_function(account: Starknet):
    exist_contracts = get_used_contracts_list(account.address_original)
    filtered_contracts = [value for key, value in ALL_CONTRACT_FUNCTIONS.items() if hex(key) not in exist_contracts]

    if len(filtered_contracts):
        random_fn = random.choice(filtered_contracts)

        if isinstance(random_fn, list):
            logger.info(
                f'[{account._id}][{account.address_original}] Random chosen: "{random_fn[0].__name__}". Unused contracts left: {len(filtered_contracts)}')
            run_script_one(account, random_fn[0], '', [])

            sleeping(30, 120)
            run_script_one(account, random_fn[1], '', [])

        elif random_fn.__name__ in SWAP_ROUTES:
            f_name = random_fn.__name__
            csv_name_1 = 'random_swap_1'
            csv_name_2 = 'random_swap_2'
            start_csv(csv_name_1)
            start_csv(csv_name_2)

            logger.info(
                f'[{account._id}][{account.address_original}] Random chosen: "{f_name}". Unused contracts left: {len(filtered_contracts)}')
            extracted_route = {f_name: SWAP_ROUTES[f_name]}
            run_random_swap_one(account, extracted_route, '', csv_name_1, csv_name_2)

        else:
            logger.info(
                f'[{account._id}][{account.address_original}] Random chosen: "{random_fn.__name__}". Unused contracts left: {len(filtered_contracts)}')
            run_script_one(account, random_fn, '', [], 'run_random_unused_function')
    else:
        logger.info(f'[{account._id}][{account.address_original}] No unused contracts left')
