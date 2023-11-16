import time
from datetime import datetime
from loguru import logger
from common import TOKEN_ADDRESS
from helpers.common import int_to_wei, wei_to_int, get_min_balance_eth
from helpers.csv_helper import write_csv_success, start_csv
from helpers.starknet import Starknet


def transfer_eth(account: Starknet, recipient, amount: float):
    min_transaction_amount = 0.00001

    retry = 0
    while True:
        if retry > 3:
            logger.error(f"Insufficient funds for transfer, skip")
            return
        retry += 1

        balance_wei = account.get_eth_balance()
        if not amount:
            tx_fee = int_to_wei(0.00007)
            amount_wei = balance_wei - int_to_wei(get_min_balance_eth()) - tx_fee
            break
        else:
            amount_wei = int_to_wei(amount)
            min_amount = amount_wei + int_to_wei(get_min_balance_eth())
            if min_amount > balance_wei:
                logger.error(f"Insufficient funds: {wei_to_int(balance_wei)} < {wei_to_int(min_amount)} ETH, retry...")
                time.sleep(5)
                continue
            break

    logger.info(f"[{account._id}][{account.address_original}] Transfer {wei_to_int(amount_wei)} ETH to {recipient}")

    if amount_wei < int_to_wei(min_transaction_amount):
        logger.error(f"Too small transaction amount, skip")
        return

    contract = account.get_contract(TOKEN_ADDRESS["ETH"])
    transfer_call = contract.functions["transfer"].prepare(int(recipient, 16), amount_wei)

    transaction = account.sign_transaction([transfer_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        account.wait_until_tx_finished(transaction_response.transaction_hash)

        csv_name = 'exchange_deposit'
        start_csv(csv_name)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        write_csv_success(account._id, {
            'status': 1,
            'csv_name': csv_name,
            'function': 'transfer_eth',
            'date': formatted_datetime,
        })
