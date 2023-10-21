import time
from loguru import logger
from helpers.starknet import Starknet


def one_wallet_tx_count(account: Starknet):
    try:
        nonce = account.account.get_nonce_sync()
        logger.info(f"[{account._id}][{account.address_original}] Transactions: {nonce}")

    except Exception:
        time.sleep(1)
        one_wallet_tx_count(account)
