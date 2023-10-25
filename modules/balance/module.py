from loguru import logger
from helpers.common import get_private_keys
from modules.balance.functions import one_wallet_balance
from helpers.cli import print_input_contract_address
from helpers.starknet import Starknet


def interface_check_balance():
    contract_address = print_input_contract_address()
    logger.info("Check Balances")

    total = 0
    for _id, wallet in enumerate(get_private_keys()):
        account = Starknet(_id, wallet)
        balance = one_wallet_balance(account, contract_address)
        total += float(balance)

    logger.info(f"TOTAL: {total}")
