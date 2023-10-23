import random
import sys
import time
from tqdm import tqdm
from loguru import logger
from termcolor import cprint
from common import TOKEN_ADDRESS

logger.remove()
logger.add(sys.stderr, format="<green>{time:MM-DD HH:mm:ss}</green> | <level>{level:<8}</level>| <level>{message}</level>")


def sleeping(from_sleep: int, to_sleep: int):
    x = random.randint(from_sleep, to_sleep)
    for _ in tqdm(range(x), desc='sleep', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)


def print_input_contract_address(title: str = 'Contract address / symbol'):
    try:
        while True:
            cprint(f'>>> {title} / empty for native:', 'yellow')
            contract_address = input("> ")

            if 0 < len(contract_address) < 5:
                if TOKEN_ADDRESS.get(contract_address.upper()):
                    return TOKEN_ADDRESS.get(contract_address.upper())
                else:
                    cprint(f'Wrong contract symbol. Please try again.\n', 'red')
                    continue
            elif len(contract_address) == 66:
                return int(contract_address, 16)
            elif len(contract_address) == 0:
                return TOKEN_ADDRESS.get('ETH')

            cprint(f'Wrong contract address. Please try again.\n', 'red')
            continue
    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit


def print_input_amounts_range(title: str = 'Swap amount'):
    try:
        while True:
            cprint(f'>>> {title} (number / range / empty = ALL):', 'yellow')
            return input("> ")
    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit


def get_amount_in_range(amount: str, check_range: bool = True) -> float:
    if 'e-' in amount:
        amount = float(amount)
    elif check_range and amount != 0 and len(amount) and '-' in amount:
        amount_from, amount_to = amount.split('-')
        diff = float(amount_to) - float(amount_from)
        amount = round(random.uniform(float(amount_from), float(amount_to)), 5 if diff <= 1 else 3)

    try:
        amount = float(amount)
    except ValueError:
        return 0

    return amount
