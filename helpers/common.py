import csv
import random
import time
from datetime import datetime

import requests
from loguru import logger
from termcolor import cprint

from common import TOKEN_ADDRESS, ZETH_TOKEN_ADDRESS
from config.settings import CEX_DEFAULT, USE_SHUFFLE, MIN_BALANCE_ETH
from helpers.csv_helper import get_csv_separator


def int_to_wei(qty, decimal=18):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))


def wei_to_int(qty, decimal=18):
    return qty / int("".join((["1"] + ["0"] * decimal)))


# 2023-08-15 22:36 format
def wait_schedule(scheduled_time, interval_time=30):
    while True:
        scheduled_datetime = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M')
        current_datetime = datetime.now()
        logger.info(f'Current timestamp: {current_datetime} | Scheduled: {scheduled_datetime}')

        if current_datetime >= scheduled_datetime:
            break
        time.sleep(interval_time)


def get_private_keys():
    with open('config/wallets.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=get_csv_separator())
        private_keys = [
            {
                "index": index,
                "starknet_private_key": row['starknet_private_key'].strip(),
                "starknet_address": row['starknet_address'].strip(),
                "web3_private_key": row['web3_private_key'].strip(),
                'recipient': ""
            } for index, row in enumerate(reader) if row['starknet_private_key'].strip()]

    if len(private_keys) == 0:
        logger.error("No private keys found in wallets.csv")

    if USE_SHUFFLE:
        random.shuffle(private_keys)

    return private_keys


def get_private_keys_recipients(key: str = f'{CEX_DEFAULT}_address'):
    with open('config/wallets.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=get_csv_separator())
        result_map = [{
            "index": index,
            'starknet_private_key': row['starknet_private_key'].strip(),
            "starknet_address": row['starknet_address'].strip(),
            "web3_private_key": row['web3_private_key'].strip(),
            'recipient': row[key].strip()
        } for index, row in enumerate(reader) if row['starknet_private_key'].strip()]

    for wallet in result_map:
        if not wallet['recipient']:
            logger.error(f"Empty recipient in config/wallets.csv for {CEX_DEFAULT}")
            raise Exception("Empty recipient error, stop process")

    if USE_SHUFFLE:
        random.shuffle(result_map)

    return result_map


def get_proxy_list():
    with open("config/proxies.txt", "r") as f:
        recipients = [row.strip() for row in f]
    if len(recipients) == 0:
        cprint("No proxy found in config/proxies.txt", "red")
    return recipients


def get_random_proxy():
    proxies = {}
    proxy_list = get_proxy_list()
    if len(proxy_list) > 0:
        proxy = random.choice(proxy_list)
        proxies = {
            'http': proxy,
            'https': proxy,
        }

    return proxies


def all_prices():
    currency_price = []
    proxies = get_random_proxy()
    response = requests.get(url=f'https://api.gateio.ws/api/v4/spot/tickers', proxies=proxies)
    currency_price.append(response.json())
    return currency_price


def price_token(currency_price, symbol):
    price = 0
    for currency in currency_price[0]:
        if currency['currency_pair'] == f'{symbol}_USDT':
            price = currency['last']
    if symbol in ['USDC', 'USDT', 'DAI', 'BUSD']:
        price = 1
    return price


def get_max_swap_amount_limited_dex(token_address, amount: float):
    max_amount = 0
    if token_address == TOKEN_ADDRESS['ETH'] or token_address == ZETH_TOKEN_ADDRESS:
        max_amount = 0.1
    elif token_address in [TOKEN_ADDRESS['USDC'], TOKEN_ADDRESS['USDT'], TOKEN_ADDRESS['DAI']]:
        max_amount = 200
    elif token_address == TOKEN_ADDRESS['WBTC']:
        max_amount = 0.007

    if amount > max_amount:
        raise Exception(f"Amount '{amount}' is too big, you can lost your money on this DEX (no liquidity)")


def get_min_balance_eth():
    if type(MIN_BALANCE_ETH) == list:
        return random.uniform(MIN_BALANCE_ETH[0], MIN_BALANCE_ETH[1])
    return MIN_BALANCE_ETH
